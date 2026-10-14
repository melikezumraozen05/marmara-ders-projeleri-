using System;
using System.Collections.Generic;
using System.Drawing;
using System.Windows.Forms;

namespace hafta3
{
    public partial class Form1 : Form
    {
        private ListBox sehirListesi = new ListBox();
        private ListBox sonucListesi = new ListBox();
        private List<string> secilenler = new List<string>();

        public Form1()
        {
            InitializeComponent();

            Text = "Şehir Seçimi";
            ClientSize = new Size(620, 350);
            StartPosition = FormStartPosition.CenterScreen;

            Label baslik1 = new Label();
            baslik1.Text = "Şehirleri istediğin sırayla seç";
            baslik1.Location = new Point(25, 25);
            baslik1.AutoSize = true;

            sehirListesi.Location = new Point(25, 60);
            sehirListesi.Size = new Size(210, 220);
            sehirListesi.SelectionMode = SelectionMode.MultiSimple;
            sehirListesi.Items.AddRange(new object[]
            {
                "Rize", "Bitlis", "Yozgat", "İstanbul", "Ankara"
            });
            sehirListesi.SelectedIndexChanged += SehirSecildi;

            Button aktarButonu = new Button();
            aktarButonu.Text = "button3";
            aktarButonu.Location = new Point(255, 130);
            aktarButonu.Size = new Size(105, 45);
            aktarButonu.Click += Aktar;

            Label baslik2 = new Label();
            baslik2.Text = "Seçim sırasına göre şehirler";
            baslik2.Location = new Point(380, 25);
            baslik2.AutoSize = true;

            sonucListesi.Location = new Point(380, 60);
            sonucListesi.Size = new Size(210, 220);

            Label bilgi = new Label();
            bilgi.Text = "Seçimi kaldırmak için şehre tekrar tıklayabilirsin.";
            bilgi.Location = new Point(25, 300);
            bilgi.AutoSize = true;

            Button button1 = new Button();
            button1.Text = "button1";
            button1.Location = new Point(255, 65);
            button1.Size = new Size(105, 40);
            Controls.Add(button1);

            Button button2 = new Button();
            button2.Text = "button2";
            button2.Location = new Point(255, 195);
            button2.Size = new Size(105, 40);
            Controls.Add(button2);

            Controls.Add(baslik1);
            Controls.Add(sehirListesi);
            Controls.Add(aktarButonu);
            Controls.Add(baslik2);
            Controls.Add(sonucListesi);
            Controls.Add(bilgi);
        }

        private void SehirSecildi(object sender, EventArgs e)
        {
            // Seçimi kaldırılan şehirleri çıkar.
            for (int i = secilenler.Count - 1; i >= 0; i--)
            {
                if (!sehirListesi.SelectedItems.Contains(secilenler[i]))
                    secilenler.RemoveAt(i);
            }

            // Yeni seçilen şehirleri sıranın sonuna ekle.
            foreach (object item in sehirListesi.SelectedItems)
            {
                string sehir = item.ToString();

                if (!secilenler.Contains(sehir))
                    secilenler.Add(sehir);
            }
        }

        private void Aktar(object sender, EventArgs e)
        {
            sonucListesi.Items.Clear();

            foreach (string sehir in secilenler)
                sonucListesi.Items.Add(sehir);
        }
    }
}