###########################################################
# Author  : Hwx                                           #
# Date    : 2016-11-22                                    #
# Name    : Chrysanthemum_figure                          #
# Version : v2                                            #
# Description : Chrysanthemum cluster                     #
###########################################################



import os, sys
import random as rd
import pandas as pd
from PIL import Image, ImageDraw, ImageFont



class Chrysanthemum_figure:
    def __init__(self):

        # Collect parameters from input
        arg_SP = None
        arg_output = None
        args = [arg_SP, arg_output]

        n = 0
        for arg in sys.argv[1:]:
            args[n] = arg
            n += 1

        # Usage
        usage = "       python Chrysanthemum_figure_v2.py <spreadsheet of all groups> <output path> "
        if args[0] == None or args[1] == None:
            print
            print 'Usage-Example Command:'
            print usage
            print
            print "Note : Inputfile = *.csv"
            exit()

        # Source
        self.SP = pd.read_csv(args[0])
        self.output_path = args[1] + '/Chrysanthemum_figure.png'

        # Backgroud
        bg_x = 6000
        bg_y = 6000
        bg_alpha = 0
        self.bg_size = (bg_x, bg_y)
        self.bg_color = (250, 250, 250, bg_alpha)

        # Ellipse
        # self.elp_sum  = 30
        self.elp_size  = (int(bg_x * 0.52 + 2), int(bg_y * 0.1 + 2))
        self.elp_alpha = 120

        # Central circle
        self.cenC_locSize = [(int(bg_x * 0.45), int(bg_y * 0.45)), (int(bg_x * 0.55), int(bg_y * 0.55))]
        self.cenC_alpha = 240
        self.cenC_color = (210, 220, 240, self.cenC_alpha)
        self.cenT_locSize = [(int(bg_x * 0.45), int(bg_y * 0.45)), (int(bg_x * 0.55), int(bg_y * 0.55))]

        # Font
        font_size = int(bg_x * 0.02)
        font 	  = "/usr/share/fonts/dejavu-lgc/DejaVuLGCSans-Bold.ttf"
        self.font_in     = ImageFont.truetype(font=font, size=font_size)
        self.font_out    = ImageFont.truetype(font=font, size=int(bg_x * 0.015))
        self.font_center = ImageFont.truetype(font=font,size=font_size)

        self.font_color = (0, 0, 0)

    def venn_SP(self):

        self.text_in = []
        df = self.SP

        sel = set()
        for i in range(len(df.columns)):
            if i == 0:
                sel = set(list(df.ix[:, i]))

            self.text_in.append(len(df.ix[:, i].dropna()))
            s = set(list(df.ix[:, i]))
            sel = sel.intersection(s)

        self.text_out = list(df.columns.values)
        self.text_cen = str(len(sel))
        self.elp_sum = len(self.text_out)


    def venn_MP(self):

        df = []
        self.text_out = []
        self.text_in = []
        self.sample_count = None
        self.inter_sum = None

        fList = sorted(os.listdir("."))
        for f in fList:
            if f.endswith(".txt"):
                df.append(pd.read_csv(f, header=None))
                self.text_in.append(len(df[-1]))
                self.text_out.append(f.split(".")[0])

        df_m = df[-1]
        for i in range(len(df) - 1):
            df_m = pd.merge(df_m, df[i])

        self.text_cen = str(len(df_m))
        self.elp_sum = len(self.text_out)
        print self.text_out

    def draw(self):

        bg = Image.new('RGBA', self.bg_size)
        bg_elp = Image.new('RGBA', self.bg_size, self.bg_color)
        bg_x, bg_y = bg.size

        elp = Image.new('RGBA', self.elp_size, (0, 0, 0, 0))
        elp_x, elp_y = elp.size

        self.elp_roAgl = 360 / self.elp_sum

        textIn_loc = (elp_x * 0.55, elp_y * 0.38)
        textOut_loc = (elp_x * 0.75, elp_y * 0.38)

        R = 0
        G = 0
        B = 0
        elp_color = (R, G, B, 0)

        import time
        for i in range(self.elp_sum):
            R = int(rd.uniform(10, 240))
            G = int(rd.uniform(10, 240))
            B = int(rd.uniform(10, 240))

            while abs(elp_color[0] - R) <= 30 or abs(elp_color[1] - G) <= 30 or abs(elp_color[2] - B) <= 30 or abs(
                            R - G) <= 10 or abs(R - B) <= 10 or abs(B - G) <= 10:
                R = int(rd.uniform(10, 240))
                G = int(rd.uniform(10, 240))
                B = int(rd.uniform(10, 240))

            elp_color = (R, G, B, 0)
            print "Color(RGB) of petal : ", elp_color

            draw = ImageDraw.Draw(elp)
            draw.ellipse([(1, 1), (elp_x * 0.7 - 1, elp_y - 1)], fill=(R, G, B, self.elp_alpha))
            draw.ellipse([(elp_x * 0.75 + 1, elp_y * 0.1 + 1), (elp_x - 1, elp_y * 0.9 - 1)], fill=elp_color,
                         outline=None)
            draw.text(textIn_loc, str(self.text_in[i]), fill='black', font=self.font_in)
            draw.text(textOut_loc, self.text_out[i], fill='black', font=self.font_out)

            elp_loc = (int(bg_x * 0.45), int(bg_y * 0.5 - 0.5 * elp_y), int(bg_x * 0.45 + elp_x), int(bg_y * 0.5 + 0.5 * elp_y))

            bg_elp.paste(elp, elp_loc, elp)
            bg_elp = bg_elp.rotate(self.elp_roAgl)

        cC = Image.new("RGBA", (int(bg_x * 0.1), int(bg_y * 0.1)))
        draw = ImageDraw.Draw(cC)
        x_c, y_c = cC.size
        draw.ellipse([(1, 1), (x_c - 1, y_c - 1)], fill=self.cenC_color)
        draw.multiline_text((x_c * 0.3, y_c * 0.40), self.text_cen, fill='black', font=self.font_center, align='center')

        bg.paste(bg_elp)
        bg.paste(cC, (int(bg_x * 0.45), int(bg_y * 0.45), int(bg_x * 0.55), int(bg_y * 0.55)), cC)
        bg.save(self.output_path)
        print "Finished the job."


Chry_fig = Chrysanthemum_figure()
if __name__ == "__main__":
    Chry_fig.venn_SP()
    Chry_fig.draw()