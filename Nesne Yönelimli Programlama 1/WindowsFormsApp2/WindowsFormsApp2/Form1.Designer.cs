namespace WindowsFormsApp2
{
    partial class Form1
    {
        /// <summary>
        ///Gerekli tasarımcı değişkeni.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///Kullanılan tüm kaynakları temizleyin.
        /// </summary>
        ///<param name="disposing">yönetilen kaynaklar dispose edilmeliyse doğru; aksi halde yanlış.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer üretilen kod

        /// <summary>
        /// Tasarımcı desteği için gerekli metot - bu metodun 
        ///içeriğini kod düzenleyici ile değiştirmeyin.
        /// </summary>
        private void InitializeComponent()
        {
            this.txtEkran = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.button3 = new System.Windows.Forms.Button();
            this.button4 = new System.Windows.Forms.Button();
            this.button5 = new System.Windows.Forms.Button();
            this.button6 = new System.Windows.Forms.Button();
            this.button7 = new System.Windows.Forms.Button();
            this.button8 = new System.Windows.Forms.Button();
            this.button9 = new System.Windows.Forms.Button();
            this.button10 = new System.Windows.Forms.Button();
            this.button11 = new System.Windows.Forms.Button();
            this.button12 = new System.Windows.Forms.Button();
            this.button13 = new System.Windows.Forms.Button();
            this.button14 = new System.Windows.Forms.Button();
            this.button15 = new System.Windows.Forms.Button();
            this.button16 = new System.Windows.Forms.Button();
            this.button17 = new System.Windows.Forms.Button();
            this.button18 = new System.Windows.Forms.Button();
            this.button19 = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // txtEkran
            // 
            this.txtEkran.Location = new System.Drawing.Point(178, 74);
            this.txtEkran.Name = "txtEkran";
            this.txtEkran.ReadOnly = true;
            this.txtEkran.Size = new System.Drawing.Size(220, 22);
            this.txtEkran.TabIndex = 0;
            this.txtEkran.Text = "0";
            this.txtEkran.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.txtEkran.TextChanged += new System.EventHandler(this.textBox1_TextChanged);
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(352, 227);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(46, 57);
            this.button1.TabIndex = 2;
            this.button1.Text = "+";
            this.button1.UseVisualStyleBackColor = true;
            // 
            // button2
            // 
            this.button2.Location = new System.Drawing.Point(350, 291);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(48, 62);
            this.button2.TabIndex = 3;
            this.button2.Text = "-";
            this.button2.UseVisualStyleBackColor = true;
            // 
            // button3
            // 
            this.button3.Location = new System.Drawing.Point(350, 163);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(48, 57);
            this.button3.TabIndex = 4;
            this.button3.Text = "*";
            this.button3.UseVisualStyleBackColor = true;
            // 
            // button4
            // 
            this.button4.Location = new System.Drawing.Point(350, 102);
            this.button4.Name = "button4";
            this.button4.Size = new System.Drawing.Size(48, 55);
            this.button4.TabIndex = 5;
            this.button4.Text = "/";
            this.button4.UseVisualStyleBackColor = true;
            // 
            // button5
            // 
            this.button5.Location = new System.Drawing.Point(236, 358);
            this.button5.Name = "button5";
            this.button5.Size = new System.Drawing.Size(50, 46);
            this.button5.TabIndex = 7;
            this.button5.Text = "0";
            this.button5.UseVisualStyleBackColor = true;
            this.button5.Click += new System.EventHandler(this.button5_Click);
            // 
            // button6
            // 
            this.button6.Location = new System.Drawing.Point(178, 290);
            this.button6.Name = "button6";
            this.button6.Size = new System.Drawing.Size(52, 62);
            this.button6.TabIndex = 8;
            this.button6.Text = "1";
            this.button6.UseVisualStyleBackColor = true;
            // 
            // button7
            // 
            this.button7.Location = new System.Drawing.Point(292, 359);
            this.button7.Name = "button7";
            this.button7.Size = new System.Drawing.Size(106, 46);
            this.button7.TabIndex = 9;
            this.button7.Text = "=";
            this.button7.UseVisualStyleBackColor = true;
            // 
            // button8
            // 
            this.button8.Location = new System.Drawing.Point(236, 290);
            this.button8.Name = "button8";
            this.button8.Size = new System.Drawing.Size(50, 62);
            this.button8.TabIndex = 10;
            this.button8.Text = "2";
            this.button8.UseVisualStyleBackColor = true;
            // 
            // button9
            // 
            this.button9.Location = new System.Drawing.Point(292, 291);
            this.button9.Name = "button9";
            this.button9.Size = new System.Drawing.Size(52, 62);
            this.button9.TabIndex = 11;
            this.button9.Text = "3";
            this.button9.UseVisualStyleBackColor = true;
            // 
            // button10
            // 
            this.button10.Location = new System.Drawing.Point(178, 227);
            this.button10.Name = "button10";
            this.button10.Size = new System.Drawing.Size(52, 58);
            this.button10.TabIndex = 12;
            this.button10.Text = "4";
            this.button10.UseVisualStyleBackColor = true;
            // 
            // button11
            // 
            this.button11.Location = new System.Drawing.Point(236, 226);
            this.button11.Name = "button11";
            this.button11.Size = new System.Drawing.Size(50, 58);
            this.button11.TabIndex = 13;
            this.button11.Text = "5";
            this.button11.UseVisualStyleBackColor = true;
            // 
            // button12
            // 
            this.button12.Location = new System.Drawing.Point(292, 227);
            this.button12.Name = "button12";
            this.button12.Size = new System.Drawing.Size(52, 58);
            this.button12.TabIndex = 14;
            this.button12.Text = "6";
            this.button12.UseVisualStyleBackColor = true;
            this.button12.Click += new System.EventHandler(this.button12_Click);
            // 
            // button13
            // 
            this.button13.Location = new System.Drawing.Point(178, 163);
            this.button13.Name = "button13";
            this.button13.Size = new System.Drawing.Size(52, 57);
            this.button13.TabIndex = 15;
            this.button13.Text = "7";
            this.button13.UseVisualStyleBackColor = true;
            this.button13.Click += new System.EventHandler(this.button13_Click);
            // 
            // button14
            // 
            this.button14.Location = new System.Drawing.Point(236, 163);
            this.button14.Name = "button14";
            this.button14.Size = new System.Drawing.Size(50, 57);
            this.button14.TabIndex = 16;
            this.button14.Text = "8";
            this.button14.UseVisualStyleBackColor = true;
            // 
            // button15
            // 
            this.button15.Location = new System.Drawing.Point(292, 163);
            this.button15.Name = "button15";
            this.button15.Size = new System.Drawing.Size(52, 57);
            this.button15.TabIndex = 17;
            this.button15.Text = "9";
            this.button15.UseVisualStyleBackColor = true;
            // 
            // button16
            // 
            this.button16.Location = new System.Drawing.Point(178, 102);
            this.button16.Name = "button16";
            this.button16.Size = new System.Drawing.Size(52, 55);
            this.button16.TabIndex = 18;
            this.button16.Text = "C";
            this.button16.UseVisualStyleBackColor = true;
            // 
            // button17
            // 
            this.button17.Location = new System.Drawing.Point(236, 102);
            this.button17.Name = "button17";
            this.button17.Size = new System.Drawing.Size(50, 55);
            this.button17.TabIndex = 19;
            this.button17.Text = "<-";
            this.button17.UseVisualStyleBackColor = true;
            // 
            // button18
            // 
            this.button18.Location = new System.Drawing.Point(292, 102);
            this.button18.Name = "button18";
            this.button18.Size = new System.Drawing.Size(52, 55);
            this.button18.TabIndex = 20;
            this.button18.Text = "%";
            this.button18.UseVisualStyleBackColor = true;
            // 
            // button19
            // 
            this.button19.Location = new System.Drawing.Point(178, 358);
            this.button19.Name = "button19";
            this.button19.Size = new System.Drawing.Size(52, 46);
            this.button19.TabIndex = 21;
            this.button19.Text = ",";
            this.button19.UseVisualStyleBackColor = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 450);
            this.Controls.Add(this.button19);
            this.Controls.Add(this.button18);
            this.Controls.Add(this.button17);
            this.Controls.Add(this.button16);
            this.Controls.Add(this.button15);
            this.Controls.Add(this.button14);
            this.Controls.Add(this.button13);
            this.Controls.Add(this.button12);
            this.Controls.Add(this.button11);
            this.Controls.Add(this.button10);
            this.Controls.Add(this.button9);
            this.Controls.Add(this.button8);
            this.Controls.Add(this.button7);
            this.Controls.Add(this.button6);
            this.Controls.Add(this.button5);
            this.Controls.Add(this.button4);
            this.Controls.Add(this.button3);
            this.Controls.Add(this.button2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.txtEkran);
            this.Name = "Form1";
            this.Text = "HesapMakinesiOdev";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TextBox txtEkran;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Button button2;
        private System.Windows.Forms.Button button3;
        private System.Windows.Forms.Button button4;
        private System.Windows.Forms.Button button5;
        private System.Windows.Forms.Button button6;
        private System.Windows.Forms.Button button7;
        private System.Windows.Forms.Button button8;
        private System.Windows.Forms.Button button9;
        private System.Windows.Forms.Button button10;
        private System.Windows.Forms.Button button11;
        private System.Windows.Forms.Button button12;
        private System.Windows.Forms.Button button13;
        private System.Windows.Forms.Button button14;
        private System.Windows.Forms.Button button15;
        private System.Windows.Forms.Button button16;
        private System.Windows.Forms.Button button17;
        private System.Windows.Forms.Button button18;
        private System.Windows.Forms.Button button19;
    }
}

