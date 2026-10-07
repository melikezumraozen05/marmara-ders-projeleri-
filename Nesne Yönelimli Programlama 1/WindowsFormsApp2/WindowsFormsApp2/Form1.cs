using System;
using System.Windows.Forms;

namespace WindowsFormsApp2
{
    public partial class Form1 : Form
    {
        TextBox ekran;

        public Form1()
        {
            InitializeComponent();

            foreach (Control kontrol in Controls)
            {
                if (kontrol is TextBox)
                    ekran = (TextBox)kontrol;
            }

            if (ekran != null)
            {
                ekran.Text = "0";
                ekran.ReadOnly = true;
                ekran.TextAlign = HorizontalAlignment.Right;
            }
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {
        }

        private void button5_Click(object sender, EventArgs e)
        {
            if (ekran == null) return;

            string rakam = ((Button)sender).Text.Trim();
            if (rakam.Length != 1 || !char.IsDigit(rakam[0]))
                return;

            if (ekran.Text == "0")
                ekran.Text = "";

            if (ekran.Text.Length < 12)
                ekran.Text += rakam;
        }

        private void button12_Click(object sender, EventArgs e)
        {
            if (ekran == null) return;

            string rakam = ((Button)sender).Text.Trim();
            if (rakam.Length != 1 || !char.IsDigit(rakam[0]))
                return;

            if (ekran.Text == "0")
                ekran.Text = "";

            if (ekran.Text.Length < 12)
                ekran.Text += rakam;
        }

        private void button13_Click(object sender, EventArgs e)
        {
            if (ekran == null) return;

            string rakam = ((Button)sender).Text.Trim();
            if (rakam.Length != 1 || !char.IsDigit(rakam[0]))
                return;

            if (ekran.Text == "0")
                ekran.Text = "";

            if (ekran.Text.Length < 12)
                ekran.Text += rakam;
        }
    }
}