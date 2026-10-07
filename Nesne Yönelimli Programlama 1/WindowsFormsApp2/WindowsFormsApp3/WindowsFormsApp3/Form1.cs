using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace WindowsFormsApp3
{
    public partial class Form1 : Form
    {
        TextBox txtEkran;
        double sayi1 = 0;
        string islem = "";
        bool yeniSayi = true;

        public Form1()
        {
            InitializeComponent();
            TasarimOlustur();
        }

        private void TasarimOlustur()
        {
            this.Text = "Hesap Makinesi";
            this.ClientSize = new Size(380, 520);
            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.StartPosition = FormStartPosition.CenterScreen;

            // Ekran (TextBox)
            txtEkran = new TextBox();
            txtEkran.Location = new Point(15, 15);
            txtEkran.Size = new Size(350, 45);
            txtEkran.Font = new Font("Segoe UI", 22);
            txtEkran.TextAlign = HorizontalAlignment.Right;
            txtEkran.ReadOnly = true;
            txtEkran.Text = "0";
            this.Controls.Add(txtEkran);

            // Buton düzeni (4 sütun x 5 satır)
            string[,] tuslar = {
                { "C", "<-", "%", "/" },
                { "7", "8",  "9", "*" },
                { "4", "5",  "6", "+" },
                { "1", "2",  "3", "-" },
                { ",", "0",  "=", ""  }
            };

            int boyut = 80, bosluk = 8, baslaX = 15, baslaY = 75;

            for (int satir = 0; satir < 5; satir++)
            {
                for (int sutun = 0; sutun < 4; sutun++)
                {
                    string yazi = tuslar[satir, sutun];
                    if (yazi == "") continue;

                    Button btn = new Button();
                    btn.Text = yazi;
                    btn.Font = new Font("Segoe UI", 20);
                    btn.Location = new Point(baslaX + sutun * (boyut + bosluk),
                                             baslaY + satir * (boyut + bosluk));
                    btn.Size = new Size(boyut, boyut);

                    // "=" butonu iki hücre genişliğinde
                    if (yazi == "=")
                        btn.Size = new Size(boyut * 2 + bosluk, boyut);

                    btn.Click += Buton_Click;
                    this.Controls.Add(btn);
                }
            }
        }

        private void Buton_Click(object sender, EventArgs e)
        {
            string tus = ((Button)sender).Text;

            if (char.IsDigit(tus[0]))              // 0-9
            {
                if (yeniSayi || txtEkran.Text == "0")
                    txtEkran.Text = tus;
                else
                    txtEkran.Text += tus;
                yeniSayi = false;
            }
            else if (tus == ",")                   // ondalık
            {
                if (yeniSayi)
                {
                    txtEkran.Text = "0,";
                    yeniSayi = false;
                }
                else if (!txtEkran.Text.Contains(","))
                    txtEkran.Text += ",";
            }
            else if (tus == "C")                   // temizle
            {
                txtEkran.Text = "0";
                sayi1 = 0;
                islem = "";
                yeniSayi = true;
            }
            else if (tus == "<-")                  // geri sil
            {
                if (!yeniSayi && txtEkran.Text.Length > 1)
                    txtEkran.Text = txtEkran.Text.Substring(0, txtEkran.Text.Length - 1);
                else
                    txtEkran.Text = "0";
            }
            else if (tus == "%")                   // yüzde
            {
                double d;
                if (double.TryParse(txtEkran.Text, out d))
                    txtEkran.Text = (d / 100).ToString();
                yeniSayi = true;
            }
            else if (tus == "+" || tus == "-" || tus == "*" || tus == "/")
            {
                double.TryParse(txtEkran.Text, out sayi1);   // sayı 1
                islem = tus;
                yeniSayi = true;
            }
            else if (tus == "=")                   // sonucu göster
            {
                if (islem == "") return;

                double sayi2;
                double.TryParse(txtEkran.Text, out sayi2);   // sayı 2
                double sonuc = 0;

                switch (islem)
                {
                    case "+": sonuc = sayi1 + sayi2; break;
                    case "-": sonuc = sayi1 - sayi2; break;
                    case "*": sonuc = sayi1 * sayi2; break;
                    case "/":
                        if (sayi2 == 0)
                        {
                            MessageBox.Show("Sıfıra bölünemez!");
                            txtEkran.Text = "0";
                            islem = "";
                            yeniSayi = true;
                            return;
                        }
                        sonuc = sayi1 / sayi2;
                        break;
                }

                txtEkran.Text = sonuc.ToString();
                islem = "";
                yeniSayi = true;
            }
        }

    }
}
