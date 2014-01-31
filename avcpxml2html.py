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
@version: 0.0.1
'''

import sys
import xml.etree.ElementTree as ET
import codecs


# PARAMETRI
CODIFICA_XML_SORGENTE='utf-8'


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
  '''Banale funzione di conversione della data'''
  newData="n/d"
  if (data is not None):
    l = data.split('-')
    if (len(l)!=3):
      return newData
    newData = l[2] + '/' + l[1] + '/' + l[0]
    return newData
  return newData

# Radice del tracciato XML
root = tree.getroot()
# metadata tag
metadata = root.find('metadata')

# Heder HTML
foutput.write('<!DOCTYPE html>\n')
foutput.write('<html>\n')
foutput.write('<head>\n')
foutput.write('<title>' + metadata.find('titolo').text + '</title>\n')
foutput.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
foutput.write('</head>\n')
foutput.write('<body>\n')
foutput.write('<h1>' + metadata.find('entePubblicatore').text + '</h1>\n')
foutput.write('<h2>' + metadata.find('titolo').text + '</h2>\n')
foutput.write('<h3>' + metadata.find('abstract').text + '</h3>\n')
foutput.write('<p>Data pubblicazione: ' + convertiData(metadata.find('dataPubbicazioneDataset').text) + '</p>\n')
foutput.write('<p>Data ultimo aggiornamento: ' + convertiData(metadata.find('dataUltimoAggiornamentoDataset').text) + '</p>\n')
foutput.write('<p>URL XML: <a href="' + metadata.find('urlFile').text + '">' + metadata.find('urlFile').text + '</a></p>\n')
foutput.write('<p>Licenza ' + metadata.find('licenza').text + '</p>\n')

# Tabella dei lotti
foutput.write('<table border="1">\n')
foutput.write('<tr>\n<th>Lotto</th><th>Partecipanti</th><th>Aggiudicatari</th>\n</tr>\n')

#u'\u20ac'.encode('utf8')

lotti = root.find('data')
# Ciclo principale su tutti i lotti
for lotto in lotti.iter('lotto'):
  foutput.write('<tr>\n<td><strong>CIG:</strong> ')
  foutput.write(lotto.find('cig').text + '<br/>')
  foutput.write('<strong>Oggetto del bando:</strong> ')
  foutput.write(lotto.find('oggetto').text + '<br/>')
  foutput.write('<strong>Procedura di scelta del contraente:</strong> ')
  foutput.write(lotto.find('sceltaContraente').text + '<br/>')
  foutput.write('<strong>Importo di aggiudiczione:</strong> ')
  foutput.write(lotto.find('importoAggiudicazione').text + ' ' + u'\u20ac' + '<br/>')
  foutput.write('<strong>Importo delle somme liquidate:</strong> ')
  foutput.write(lotto.find('importoSommeLiquidate').text + ' ' + u'\u20ac' + '<br/>')
  foutput.write('<strong>Tempi di completamento:</strong> dal ')
  dataInizio = lotto.find('tempiCompletamento').find('dataInizio')
  dataFine = lotto.find('tempiCompletamento').find('dataUltimazione')
  if ( dataInizio is not None):
    foutput.write(convertiData(dataInizio.text))
  else:
    foutput.write('n/d')
  foutput.write(' al ')
  if (dataFine is not None):
    foutput.write(convertiData(dataFine.text))
  else:
    foutput.write('n/d')
  foutput.write('</td>\n<td>')
  foutput.write('<ul>')
  partecipanti=lotto.find('partecipanti')
  for partecipante in partecipanti.iter('partecipante'):
    foutput.write('<li><strong>Ditta:</strong> ' + partecipante.find('ragioneSociale').text + '<br/>')
    foutput.write('<strong>CF:</strong> ' + partecipante.find('codiceFiscale').text + '</li>')
  raggruppamenti = partecipanti.find('raggruppamento')
  for raggruppamento in partecipanti.iter('raggruppamento'):
    foutput.write('<li>Raggruppamento</li>')
    foutput.write('<ul>')
    for membro in raggruppamento.iter('membro'):
      foutput.write('<li><strong>Ditta:</strong> ' + membro.find('ragioneSociale').text + '<br/>')
      foutput.write('<strong>CF:</strong> ' + membro.find('codiceFiscale').text + '<br/>')
      foutput.write('<strong>Ruolo:</strong> ' + membro.find('ruolo').text + '</li>')
    foutput.write('</ul>')
  foutput.write('</ul>')
  foutput.write('</td>\n')
  foutput.write('<td>\n')
  foutput.write('<ul>\n')
  aggiudicatari=lotto.find('aggiudicatari')
  for aggiudicatario in aggiudicatari.iter('aggiudicatario'):
    foutput.write('<li><strong>Ditta:</strong> ' + aggiudicatario.find('ragioneSociale').text + '<br/>')
    foutput.write('<strong>CF:</strong> ' + aggiudicatario.find('codiceFiscale').text + '</li>')
  raggruppamenti = aggiudicatari.find('aggiudicatarioRaggruppamento')
  for raggruppamento in aggiudicatari.iter('aggiudicatarioRaggruppamento'):
    foutput.write('<li>Raggruppamento</li>')
    foutput.write('<ul>')
    for membro in raggruppamento.iter('membro'):
      foutput.write('<li><strong>Ditta:</strong> ' + membro.find('ragioneSociale').text + '<br/>')
      foutput.write('<strong>CF:</strong> ' + membro.find('codiceFiscale').text + '<br/>')
      foutput.write('<strong>Ruolo:</strong> ' + membro.find('ruolo').text + '</li>')
    foutput.write('</ul>')
  foutput.write('</ul>')
  foutput.write('</td>\n')
  foutput.write('</tr>\n')
foutput.write('</table>\n')
foutput.write('</body>\n')
foutput.write('</html>\n')
foutput.close()
