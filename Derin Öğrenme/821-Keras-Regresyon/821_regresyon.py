"""821 | Keras regresyon deneyleri. Gercek sonuc tablosunu yeniden uretir."""
from __future__ import annotations
import os
os.environ.setdefault("KERAS_BACKEND","torch")
os.environ.setdefault("OMP_NUM_THREADS","2")
import argparse, csv, json, random, time
from pathlib import Path
from dataclasses import dataclass, asdict, replace
import numpy as np
import keras
from keras import layers
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

SEED=821
HERE=Path(__file__).resolve().parent

@dataclass(frozen=True)
class Experiment:
    model_id: str
    group: str
    activation: str
    optimizer: str
    units: int=32
    hidden_layers: int=1
    batch_size: int=32
    learning_rate: float=.005
    max_epochs: int=120

def seed_all():
    random.seed(SEED)
    np.random.seed(SEED)
    keras.utils.set_random_seed(SEED)
    if keras.backend.backend()=="torch":
        import torch
        torch.set_num_threads(2)

def dataset():
    x,y=load_diabetes(return_X_y=True)
    xt,x_test,yt,y_test=train_test_split(x,y,test_size=.2,random_state=SEED)
    x_train,x_val,y_train,y_val=train_test_split(xt,yt,test_size=.2,random_state=SEED)
    xs=StandardScaler().fit(x_train)
    ys=StandardScaler().fit(y_train.reshape(-1,1))
    transform_y=lambda arr:ys.transform(arr.reshape(-1,1)).astype("float32")
    return dict(
        x_train=xs.transform(x_train).astype("float32"),
        x_val=xs.transform(x_val).astype("float32"),
        x_test=xs.transform(x_test).astype("float32"),
        y_train=transform_y(y_train),
        y_val=transform_y(y_val),
        y_test=transform_y(y_test),
        y_val_original=y_val,y_test_original=y_test,y_scaler=ys
    )

def experiments(quick=False):
    baseline=[
        Experiment(f"T{i:02d}","aktivasyon_optimizasyon",act,opt)
        for i,(act,opt) in enumerate(
            ((act,opt) for act in ("linear","sigmoid","tanh","relu")
             for opt in ("SGD","Adam","RMSprop")),1)
    ]
    ref=next(x for x in baseline if x.activation=="relu" and x.optimizer=="Adam")
    variations=[
        ("V01","noron_8",{"units":8}),
        ("V02","noron_64",{"units":64}),
        ("V03","iki_gizli_katman",{"hidden_layers":2}),
        ("V04","batch_16",{"batch_size":16}),
        ("V05","batch_64",{"batch_size":64}),
        ("V06","lr_0_001",{"learning_rate":.001}),
        ("V07","lr_0_01",{"learning_rate":.01}),
        ("V08","epoch_60",{"max_epochs":60})
    ]
    all_exp=baseline+[replace(ref,model_id=idx,group=name,**delta)
                       for idx,name,delta in variations]
    return [all_exp[0],all_exp[10],all_exp[-1]] if quick else all_exp

def model_for(exp,input_count):
    model=keras.Sequential(name="model_"+exp.model_id)
    model.add(layers.Input(shape=(input_count,)))
    for _ in range(exp.hidden_layers):
        model.add(layers.Dense(exp.units,activation=exp.activation))
    # Regresyonda cikis kisitlanmamalidir.
    model.add(layers.Dense(1,activation="linear"))
    optimizers={"SGD":keras.optimizers.SGD,
                "Adam":keras.optimizers.Adam,
                "RMSprop":keras.optimizers.RMSprop}
    model.compile(
        optimizer=optimizers[exp.optimizer](learning_rate=exp.learning_rate),
        loss="mse",metrics=["mae"])
    return model

def metrics(real,pred):
    mse=float(mean_squared_error(real,pred))
    return dict(mse=mse,rmse=float(np.sqrt(mse)),
                mae=float(mean_absolute_error(real,pred)),
                r2=float(r2_score(real,pred)))

def train(exp,d):
    keras.backend.clear_session()
    seed_all()
    model=model_for(exp,d["x_train"].shape[1])
    early=keras.callbacks.EarlyStopping(
        monitor="val_loss",patience=15,min_delta=.0001,restore_best_weights=True)
    tic=time.perf_counter()
    history=model.fit(d["x_train"],d["y_train"],
                      validation_data=(d["x_val"],d["y_val"]),
                      batch_size=exp.batch_size,epochs=exp.max_epochs,
                      callbacks=[early],verbose=0,shuffle=True)
    seconds=round(time.perf_counter()-tic,2)
    prediction=d["y_scaler"].inverse_transform(
        model.predict(d["x_val"],verbose=0)).ravel()
    m=metrics(d["y_val_original"],prediction)
    result={**asdict(exp),"epochs_trained":len(history.history["loss"]),
            "val_mse":m["mse"],"val_rmse":m["rmse"],
            "val_mae":m["mae"],"val_r2":m["r2"],"seconds":seconds}
    return result,model

def save_csv(rows,path):
    with path.open("w",encoding="utf-8-sig",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys()))
        writer.writeheader();writer.writerows(rows)

def main():
    cli=argparse.ArgumentParser()
    cli.add_argument("--quick",action="store_true")
    args=cli.parse_args()
    out=HERE/("hizli_test" if args.quick else "sonuclar")
    out.mkdir(exist_ok=True)
    d=dataset();seed_all()
    designs=experiments(args.quick)
    path=out/"821_deney_sonuclari.csv"
    existing={}
    if path.exists():
        with path.open(encoding="utf-8-sig",newline="") as f:
            for r in csv.DictReader(f):
                for k in ("learning_rate","val_mse","val_rmse","val_mae","val_r2","seconds"):
                    r[k]=float(r[k])
                for k in ("units","hidden_layers","batch_size","max_epochs","epochs_trained"):
                    r[k]=int(r[k])
                existing[r["model_id"]]=r
    result=[]
    for i,exp in enumerate(designs,1):
        if exp.model_id in existing:
            row=existing[exp.model_id]
        else:
            row,_=train(exp,d)
            existing[exp.model_id]=row
        result.append(row)
        save_csv(list(existing.values()),path)
        print(f"{i}/{len(designs)} {exp.model_id} MAE={row['val_mae']:.2f}",flush=True)
    best=min(result,key=lambda r:(r["val_mae"],r["model_id"]))
    best_exp=next(e for e in designs if e.model_id==best["model_id"])
    _,final_model=train(best_exp,d)
    testpred=d["y_scaler"].inverse_transform(
        final_model.predict(d["x_test"],verbose=0)).ravel()
    summary={
        "student_last_three":"821","seed":SEED,
        "keras_version":keras.__version__,"backend":keras.backend.backend(),
        "dataset":"sklearn.datasets.load_diabetes",
        "train_count":len(d["x_train"]),"validation_count":len(d["x_val"]),
        "test_count":len(d["x_test"]),"n_experiments":len(result),
        "best_experiment_id":best_exp.model_id,
        "best_validation_mae":best["val_mae"],
        "best_hyperparameters":asdict(best_exp),
        "final_test_metrics":metrics(d["y_test_original"],testpred)
    }
    save_csv(result,path)
    (out/"821_ozet.json").write_text(
        json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print("FINAL:",json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
