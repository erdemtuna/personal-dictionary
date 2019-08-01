#!/usr/bin/python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle, TA_CENTER, TA_LEFT
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
########################################################################
# Main Source:
# http://www.blog.pythonlibrary.org/2013/08/09/reportlab-how-to-combine-static-content-and-multipage-tables/


class DataToPDF(object):

    # ----------------------------------------------------------------------
    def __init__(self, Collection):
        '''Constructor'''
        self.width, self.height = letter
        self.styles = getSampleStyleSheet()
        self.collection = Collection

    # ----------------------------------------------------------------------
    def coord(self, x, y, unit=1):
        '''
        http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
        Helper class to help position flowables in Canvas objects
        '''
        x, y = x * unit, self.height - y * unit
        return x, y

    # ----------------------------------------------------------------------
    def run(self):
        '''
        Run the report
        '''
        self.doc = SimpleDocTemplate('VocabularyList.pdf')
        self.story = [Spacer(1, 35*mm)]
        self.createLineItems()

        self.doc.build(self.story, onFirstPage=self.createDocument)
        # print 'finished!'

    # ----------------------------------------------------------------------
    def createDocument(self, canvas, doc):
        '''
        Create the document
        '''
        self.c = canvas
        self.c.setAuthor('ErdemTuna')
        self.c.setTitle('VocabularyList')
        normal = self.styles['Normal']
        style_Title = ParagraphStyle(
            name='centered', fontName='Times-Bold', fontSize=22, alignment=TA_CENTER)
        header_text = 'Vocabulary List'
        p = Paragraph(header_text, style_Title)
        p.wrapOn(self.c, self.width, self.height)
        p.drawOn(self.c, *self.coord(0, 6, mm))

        ptext = '''This list is generated automatically.
	'''
        style_Body = ParagraphStyle(
            name='Body', fontName='Times-Roman', fontSize=11, alignment=TA_LEFT)
        p = Paragraph(ptext, style=style_Body)
        p.wrapOn(self.c, self.width-50, self.height)
        p.drawOn(self.c, *self.coord(12, 25, mm))
        ptext = '''
        Sources: theguardian.com, oxfordlearnersdictionaries.com,
        collinsdictionary.com, Financial Times
        '''
        style_Body = ParagraphStyle(
            name='Body', fontName='Times-Roman', fontSize=11, alignment=TA_LEFT)
        p = Paragraph(ptext, style=style_Body)
        p.wrapOn(self.c, self.width-50, self.height)
        p.drawOn(self.c, *self.coord(12, 35, mm))
        #p = Paragraph(ptext, style=normal)
        #p.wrapOn(self.c, self.width-50, self.height)
        #p.drawOn(self.c, 30, 600)

    # ----------------------------------------------------------------------
    def createLineItems(self):
        # register new fonts
        pdfmetrics.registerFont(
            TTFont('Inconsolata', 'fonts/Inconsolata-Regular.ttf'))
        pdfmetrics.registerFont(
            TTFont('InconsolataBold', 'fonts/Inconsolata-Bold.ttf'))
        pdfmetrics.registerFont(
            TTFont('Akrobat', 'fonts/Akrobat-Regular.ttf'))
        pdfmetrics.registerFont(
            TTFont('AkrobatBold', 'fonts/Akrobat-Bold.ttf'))

        text_data = ['_id', 'Word', 'Means', 'Use']
        d = []
        font_size = 8

        # column header formattings
        for text in text_data:
            if(text == 'Word'):
                style = ParagraphStyle(name='centered',
                                       alignment=TA_LEFT,
                                       fontName='InconsolataBold',
                                       fontSize=11
                                       )
                p = Paragraph(text, style)
                # insert to array
                d.append(p)
            elif(text == 'Means'):
                style = ParagraphStyle(name='centered',
                                       alignment=TA_LEFT,
                                       fontName='AkrobatBold',
                                       fontSize=11
                                       )
                p = Paragraph(text, style)
                # insert to array
                d.append(p)
            elif(text == 'Use'):
                style = ParagraphStyle(name='centered',
                                       alignment=TA_LEFT,
                                       fontName='InconsolataBold',
                                       fontSize=11
                                       )
                p = Paragraph(text, style)
                # insert to array
                d.append(p)
            else:
                style = ParagraphStyle(name='centered',
                                       alignment=TA_LEFT,
                                       fontName='InconsolataBold',
                                       fontSize=11
                                       )
                p = Paragraph('#', style)
                # insert to array
                d.append(p)
        # insert first row to the table
        data = [d]

        line_num = 1
        formatted_line_data = []
        line_data = ('_id', 'word', 'means', 'use')
        for document in self.collection:

            # create new row
            for key in line_data:
                style = None
                # determine cell style
                if(key == 'means'):
                    style = ParagraphStyle(name='centered',
                                           alignment=TA_LEFT,
                                           fontName='Akrobat',
                                           fontSize=11
                                           )
                else:
                    style = ParagraphStyle(name='centered',
                                           alignment=TA_LEFT,
                                           fontName='Inconsolata',
                                           fontSize=11
                                           )
                ptext = ''
                # determine cell text
                if(key == '_id'):
                    ptext = str(line_num)
                    #print('id')
                else:
                    ptext = document[key]
                    #print(ptext)
                # create text with style
                p = Paragraph(ptext, style)
                formatted_line_data.append(p)
            # add row to table
            data.append(formatted_line_data)
            formatted_line_data = []
            line_num += 1

        table = Table(data, colWidths=[35, 120, 100, 280])
        table.setStyle(TableStyle([
            ('INNERGRID', (0, 0), (-1, -1), 0.05, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.05, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        self.story.append(table)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    t = DataToPDF()
    t.run()
