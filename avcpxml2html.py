#!/bin/python

# avcpxml2html is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# avcpxml2html is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with avcpxml2html.  If not, see <http://www.gnu.org/licenses/>.

'''
Semplice programma per la conversione del file XML aderente alle specifiche
tecniche di AVCP in ottemperanza a Art.1,comma 32,L.190/2012.

Specifiche XML:
 * http://dati.avcp.it/schema/datasetAppaltiL190.xsd
 * http://dati.avcp.it/schema/TypesL190.xsd

Tested with Python 2.7

@author: Michele Mordenti
@version: 0.2
'''

import sys
import xml.etree.ElementTree as ET
import codecs
import re


# PARAMETRI
CODIFICA_XML_SORGENTE='utf-8'
INDENT = '\t' # tabulazione
#INDENT = '' # nessuna indentazione
#INDENT = '  ' # due spazi bianchi
ND = 'n/d' # rappresentazione dato non disponibile

# Leggo argomenti
if len(sys.argv)!=2 :
    print 'Specificare il nome del file contenete il tracciato record XML di AVCP'
    print 'Esempio: ' + sys.argv[0] + 'avcp_dataset_2013.xml'
    sys.exit(1)

XML_INPUT=sys.argv[1]

try:
    tree = ET.parse(XML_INPUT)
    foutput = codecs.open(XML_INPUT + '.html', 'w', encoding=CODIFICA_XML_SORGENTE)
except IOError:
    print 'Non posso aprire il file' + XML_INPUT
    sys.exit(2)


def convertiData(data):
  '''Banale funzione di conversione della data
     input: None --> output: ND
     input: "aaaa-mm-gg" --> output: "gg/mm/aaaa"
     input: "aaaa-mm-gg+hh:mm" --> output: "gg/mm/aaaa (+hh:mm)"
     input: * --> output *
  '''
  if (data is not None):
    if (re.match('^\d{4}-\d{2}-\d{2}$',data) is not None):
      p = re.compile('(\d+)-(\d+)-(\d+)')
      return p.match(data).group(3) + '/' + \
             p.match(data).group(2) + '/' + \
             p.match(data).group(1)
    if (re.match('^\d{4}-\d{2}-\d{2}\+\d{2}:\d{2}$',data) is not None):
      p = re.compile('(\d+)-(\d+)-(\d+)\+(\d+:\d+)')
      return p.match(data).group(3) + '/' + \
             p.match(data).group(2) + '/' + \
             p.match(data).group(1) + ' (+' + \
             p.match(data).group(4) + ')'
    return data
  return ND

# Radice del tracciato XML
root = tree.getroot()
# metadata tag
metadata = root.find('metadata')

# Header HTML
foutput.write('<!DOCTYPE html>\n')
foutput.write('<html>\n')
foutput.write(INDENT + '<head>\n')
titolo = metadata.find('titolo')
if (titolo.text is not None):
  foutput.write(INDENT*2 + '<title>' + titolo.text + '</title>\n')
foutput.write(INDENT*2 + '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
foutput.write(INDENT + '</head>\n')
foutput.write(INDENT + '<body>\n')
if (metadata.find('entePubblicatore').text is not None):
  foutput.write(INDENT*2 + '<h1>' + metadata.find('entePubblicatore').text + '</h1>\n')
else:
  foutput.write(INDENT*2 + '<h1>Ente ignoto</h1>\n')
if (titolo.text is not None):
  foutput.write(INDENT*2 + '<h2>' + titolo.text + '</h2>\n')
else:
  foutput.write(INDENT*2 + '<h2>titolo assente</h2>\n')
if (metadata.find('abstract').text is not None):
  foutput.write(INDENT*2 + '<h3>' + metadata.find('abstract').text + '</h3>\n')
else:
  foutput.write(INDENT*2 + '<h3>abstract assente</h3>\n')
foutput.write(INDENT*2 + '<p>Data pubblicazione: ' + convertiData(metadata.find('dataPubbicazioneDataset').text) + '</p>\n')
foutput.write(INDENT*2 + '<p>Data ultimo aggiornamento: ' + convertiData(metadata.find('dataUltimoAggiornamentoDataset').text) + '</p>\n')
if (metadata.find('urlFile').text is not None):
  foutput.write(INDENT*2 + '<p>URL XML: <a href="' + metadata.find('urlFile').text + '">' + metadata.find('urlFile').text + '</a></p>\n')
else:
  foutput.write(INDENT*2 + '<p>URL XML: assente</p>\n')
if (metadata.find('licenza').text is not None):
  foutput.write(INDENT*2 + '<p>Licenza: ' + metadata.find('licenza').text + '</p>\n')
else:
  foutput.write(INDENT*2 + '<p>Licenza: assente</p>\n')

# Tabella dei lotti
foutput.write(INDENT*2 + '<table border="1">\n')
# Intestazione
foutput.write(INDENT*3 + '<thead>\n' + INDENT*4 + '<tr>\n' +
    INDENT*5 + '<th>Lotto</th>\n' + INDENT*5 + '<th>Partecipanti</th>\n' + INDENT*5 + '<th>Aggiudicatari</th>\n' +
    INDENT*4 + '</tr>\n' + INDENT*3 + '<thead>\n' + INDENT*3 + '<tbody>\n')

lotti = root.find('data')
# Ciclo principale su tutti i lotti
for lotto in lotti.iter('lotto'):
  # Colonna lotti
  foutput.write(INDENT*4 + '<tr>\n' + INDENT*5 + '<td>\n' + INDENT* 6 + '<strong>CIG:</strong> ')
  foutput.write(lotto.find('cig').text + '<br/>\n')
  foutput.write(INDENT*6 + '<strong>Oggetto del bando:</strong> ')
  foutput.write(lotto.find('oggetto').text + '<br/>\n')
  foutput.write(INDENT*6 + '<strong>Procedura di scelta del contraente:</strong> ')
  foutput.write(lotto.find('sceltaContraente').text + '<br/>\n')
  foutput.write(INDENT*6 + '<strong>Importo di aggiudicazione:</strong> ')
  foutput.write(lotto.find('importoAggiudicazione').text + ' ' + u'\u20ac' + '<br/>\n')
  foutput.write(INDENT*6 + '<strong>Importo delle somme liquidate:</strong> ')
  foutput.write(lotto.find('importoSommeLiquidate').text + ' ' + u'\u20ac' + '<br/>\n')
  foutput.write(INDENT*6 + '<strong>Tempi di completamento:</strong> dal ')
  dataInizio = lotto.find('tempiCompletamento').find('dataInizio')
  dataFine = lotto.find('tempiCompletamento').find('dataUltimazione')
  if ( dataInizio is not None):
    foutput.write(convertiData(dataInizio.text))
  else:
    foutput.write(ND)
  foutput.write(' al ')
  if (dataFine is not None):
    foutput.write(convertiData(dataFine.text))
  else:
    foutput.write(ND)
  foutput.write('\n' + INDENT*5 + '</td>\n')
  # Colonna partecipanti
  foutput.write(INDENT*5 + '<td>\n')
  foutput.write(INDENT*6 + '<ul>\n')
  partecipanti=lotto.find('partecipanti')
  for partecipante in partecipanti.iter('partecipante'):
    foutput.write(INDENT*7 + '<li>\n' + INDENT*8 + '<strong>Ditta:</strong> ' + partecipante.find('ragioneSociale').text + '<br/>\n')
    if (partecipante.find('codiceFiscale') is not None):
      foutput.write(INDENT*8 + '<strong>C.F. :</strong> ' + partecipante.find('codiceFiscale').text + '\n' + INDENT*7 + '</li>\n')
    else:
      foutput.write(INDENT*8 + '<strong>I.F.E. :</strong> ' + partecipante.find('identificativoFiscaleEstero').text + '\n' + INDENT*7 + '</li>\n')
  for raggruppamento in partecipanti.iter('raggruppamento'):
    foutput.write(INDENT*7 + '<li>Raggruppamento\n')
    foutput.write(INDENT*8 + '<ul>\n')
    for membro in raggruppamento.iter('membro'):
      foutput.write(INDENT*9 + '<li>\n' + INDENT*10 + '<strong>Ditta:</strong> ' + membro.find('ragioneSociale').text + '<br/>\n')
      if (membro.find('codiceFiscale') is not None):
        foutput.write(INDENT*10 + '<strong>C.F. :</strong> ' + membro.find('codiceFiscale').text + '<br/>\n')
      else:
        foutput.write(INDENT*10 + '<strong>I.F.E. : </strong> ' + membro.find('identificativoFiscaleEstero').text + '<br/>\n')
      foutput.write(INDENT*10 + '<strong>Ruolo:</strong> ' + membro.find('ruolo').text + '\n' + INDENT*9 + '</li>\n')
    foutput.write(INDENT*8 + '</ul>\n')
    foutput.write(INDENT*7 + '</li>\n')
  foutput.write(INDENT*6 + '</ul>\n')
  foutput.write(INDENT*5 + '</td>\n')
  # Colonna aggiudicatari
  foutput.write(INDENT*5 + '<td>\n')
  foutput.write(INDENT*6 + '<ul>\n')
  aggiudicatari=lotto.find('aggiudicatari')
  for aggiudicatario in aggiudicatari.iter('aggiudicatario'):
    foutput.write(INDENT*7 + '<li>\n' + INDENT*8 + '<strong>Ditta:</strong> ' + aggiudicatario.find('ragioneSociale').text + '<br/>\n')
    if (aggiudicatario.find('codiceFiscale') is not None):
      foutput.write(INDENT*8 + '<strong>C.F. :</strong> ' + aggiudicatario.find('codiceFiscale').text + '\n' + INDENT*7 + '</li>\n')
    else:
      foutput.write(INDENT*8 + '<strong>I.F.E. :</strong> ' + aggiudicatario.find('identificativoFiscaleEstero').text + '\n' + INDENT*7 + '</li>\n')
  for raggruppamento in aggiudicatari.iter('aggiudicatarioRaggruppamento'):
    foutput.write(INDENT*7 + '<li>Raggruppamento\n')
    foutput.write(INDENT*8 + '<ul>\n')
    for membro in raggruppamento.iter('membro'):
      foutput.write(INDENT*9 + '<li>\n' + INDENT*10 + '<strong>Ditta:</strong> ' + membro.find('ragioneSociale').text + '<br/>\n')
      if (membro.find('codiceFiscale') is not None):
        foutput.write(INDENT*10 + '<strong>C.F. :</strong> ' + membro.find('codiceFiscale').text + '<br/>\n')
      else:
        foutput.write(INDENT*10 + '<strong>I.F.E. :</strong> ' + membro.find('identificativoFiscaleEstero').text + '<br/>\n')
      foutput.write(INDENT*10 + '<strong>Ruolo:</strong> ' + membro.find('ruolo').text + '\n' + INDENT*9 + '</li>\n')
    foutput.write(INDENT*8 + '</ul>\n')
    foutput.write(INDENT*7 + '</li>\n')
  foutput.write(INDENT*6 + '</ul>\n')
  foutput.write(INDENT*5 + '</td>\n')
  foutput.write(INDENT*4 + '</tr>\n')
foutput.write(INDENT*3 + '</tbody>\n')
foutput.write(INDENT*2 + '</table>\n')
foutput.write(INDENT + '</body>\n')
foutput.write('</html>\n')
foutput.close()
