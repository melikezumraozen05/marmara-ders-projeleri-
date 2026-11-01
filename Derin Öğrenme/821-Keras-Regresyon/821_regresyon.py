"""Tek bir Keras regresyon odevi: ogretmenin tahta notu + Odev 1.docx.
Belgedeki hedef y=1+sin(pi*y/4) belirsizdir. p girdisi varsayilmistir.
"""
import os
os.environ.setdefault("KERAS_BACKEND","torch")
os.environ.setdefault("OMP_NUM_THREADS","2")
from pathlib import Path
import csv, json, time, random
from dataclasses import dataclass, asdict, replace
import numpy as np
import keras
from keras import layers
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE=Path(__file__).resolve().parent
OUT=BASE/"sonuclar"
FIG=BASE/"grafikler"
SEED=21
EPOCHS=300

@dataclass
class Run:
    kod:str
    grup:str
    deger:str
    aktivasyon:str="ReLU"
    ogrenme_orani:float=.1
    optimizer:str="SGD"
    dagilim:str="normal"
    gizli_katman:int=1
    noron:int=2

def configurations():
    groups=[
      ("Aktivasyon","aktivasyon",["Lineer","Sigmoid","Hiperbolik Tanjant","ReLU","LeakyReLU","ELU","SiLU"]),
      ("Öğrenme oranı","ogrenme_orani",[.1,.01,.001]),
      ("Optimizasyon","optimizer",["SGD","RMSProp","ADAM"]),
      ("Başlangıç dağılımı","dagilim",["normal","uniform"]),
      ("Gizli katman sayısı","gizli_katman",[1,2,5,10,20]),
      ("Gizli nöron sayısı","noron",[2,5,10,20,50])]
    runs=[]
    for group,attribute,values in groups:
        for value in values:
            r=Run(f"D{len(runs)+1:02}",group,str(value))
            setattr(r,attribute,value)
            runs.append(r)
    return runs

def set_seed():
    random.seed(SEED);np.random.seed(SEED);keras.utils.set_random_seed(SEED)
    if keras.backend.backend()=="torch":
        import torch
        torch.manual_seed(SEED);torch.set_num_threads(2)

def network(c):
    keras.backend.clear_session()
    set_seed()
    if c.dagilim=="normal":
        init=keras.initializers.RandomNormal(mean=0,stddev=.05,seed=SEED)
    else:
        init=keras.initializers.RandomUniform(minval=-.05,maxval=.05,seed=SEED)
    m=keras.Sequential()
    m.add(layers.Input(shape=(1,)))
    activation={"Lineer":"linear","Sigmoid":"sigmoid","Hiperbolik Tanjant":"tanh","ReLU":"relu","SiLU":"silu"}
    for _ in range(c.gizli_katman):
        m.add(layers.Dense(c.noron,kernel_initializer=init,bias_initializer="zeros"))
        if c.aktivasyon in activation:
            m.add(layers.Activation(activation[c.aktivasyon]))
        elif c.aktivasyon=="LeakyReLU":
            m.add(layers.LeakyReLU(negative_slope=.3))
        elif c.aktivasyon=="ELU":
            m.add(layers.ELU(alpha=1.0))
    m.add(layers.Dense(1,activation="linear",kernel_initializer=init,bias_initializer="zeros"))
    opts={"SGD":keras.optimizers.SGD,"RMSProp":keras.optimizers.RMSprop,"ADAM":keras.optimizers.Adam}
    m.compile(optimizer=opts[c.optimizer](learning_rate=c.ogrenme_orani),loss="mse")
    return m

def train(c,p,y):
    m=network(c)
    history=[]
    snaps={}
    epochs={0,1,2,5,10,25,50,100,200,300}
    class Recorder(keras.callbacks.Callback):
        def on_train_begin(self,logs=None):
            snaps[0]=self.model.predict(p,verbose=0).ravel()
        def on_epoch_end(self,epoch,logs=None):
            history.append(float(logs["loss"]))
            if epoch+1 in epochs:
                snaps[epoch+1]=self.model.predict(p,verbose=0).ravel()
    tic=time.perf_counter()
    m.fit(p,y,epochs=EPOCHS,batch_size=len(p),shuffle=False,callbacks=[Recorder()],verbose=0)
    seconds=round(time.perf_counter()-tic,3)
    pred=m.predict(p,verbose=0).ravel()
    truth=y.ravel()
    mse=float(np.mean((truth-pred)**2))
    rmse=float(np.sqrt(mse))
    r2=float(1-sum((truth-pred)**2)/sum((truth-truth.mean())**2))
    valid=bool(np.isfinite([mse,rmse,r2]).all())
    result={"kod":c.kod,"karsilastirma":c.grup,"degisken":c.deger,
            "aktivasyon":c.aktivasyon,"ogrenme_orani":c.ogrenme_orani,
            "optimizer":c.optimizer,"dagilim":c.dagilim,
            "gizli_katman":c.gizli_katman,"noron":c.noron,
            "epoch":EPOCHS,"seed":SEED,
            "MSE":mse if valid else None,"RMSE":rmse if valid else None,
            "R2":r2 if valid else None,"sure_sn":seconds,
            "durum":"OK" if valid else "SAYISAL_KARARSIZLIK"}
    return result,history,snaps,pred

def save_csv(rows):
    with (OUT/"821_karsilastirmalar.csv").open("w",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)

def draw_best(history,snaps,p,y,pred):
    xs=np.arange(1,EPOCHS+1)
    var=float(np.mean((y-y.mean())**2))
    fig,ax=plt.subplots(figsize=(8,4))
    ax.plot(xs,np.maximum(history,1e-12));ax.set_yscale("log")
    ax.set(xlabel="Epoch",ylabel="MSE (log)",title="Epoch / MSE")
    fig.tight_layout();fig.savefig(FIG/"01_epoch_mse_log.png");plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4))
    ax.plot(xs,1-np.array(history)/var)
    ax.set(xlabel="Epoch",ylabel="R2",title="Epoch / R2")
    fig.tight_layout();fig.savefig(FIG/"02_epoch_r2.png");plt.close(fig)
    fig,ax=plt.subplots(figsize=(8,4))
    ax.plot(p,y,label="Hedef");ax.plot(p,pred,label="Tahmin")
    ax.set(xlabel="p",ylabel="y",title="Hedef / Cikis")
    ax.legend();fig.tight_layout();fig.savefig(FIG/"03_hedef_cikis.png");plt.close(fig)
    fig,axs=plt.subplots(2,5,figsize=(14,6),sharex=True,sharey=True)
    for ax,e in zip(axs.flat,[0,1,2,5,10,25,50,100,200,300]):
        ax.plot(p,y,label="Hedef");ax.plot(p,snaps[e],label="Cikis")
        ax.set_title(f"Epoch {e}")
    axs.flat[0].legend();fig.tight_layout()
    fig.savefig(FIG/"04_epoch_hedef_cikis.png");plt.close(fig)

def main():
    OUT.mkdir(exist_ok=True);FIG.mkdir(exist_ok=True)
    p=np.linspace(-2,2,201,dtype=np.float32).reshape(-1,1)
    y=(1+np.sin(np.pi*p/4)).astype(np.float32)
    rows=[]
    for c in configurations():
        row,_,_,_=train(c,p,y)
        rows.append(row);save_csv(rows)
        print(c.kod,c.grup,c.deger,"MSE",row["MSE"],flush=True)
    valid=[r for r in rows if r["MSE"] is not None]
    best=min(valid,key=lambda r:r["MSE"])
    winners={}
    for group in dict.fromkeys(r["karsilastirma"] for r in rows):
        candidates=[r for r in valid if r["karsilastirma"]==group]
        winners[group]=min(candidates,key=lambda r:r["MSE"])["kod"] if candidates else None
    config=next(c for c in configurations() if c.kod==best["kod"])
    _,h,s,pred=train(config,p,y)
    draw_best(h,s,p.ravel(),y.ravel(),pred)
    summary={"tohum":SEED,"her_deney_epoch":EPOCHS,
             "deney_sayisi":len(rows),"en_iyi_deney":best,
             "grup_birincileri":winners,
             "uyari":"Belgedeki sin(pi*y/4) ifadesi sin(pi*p/4) varsayildi; hocaya teyit."}
    (OUT/"821_ozet.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Bitti:",best["kod"],flush=True)

if __name__=="__main__":
    main()
