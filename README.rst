avcpxml2html
============

Semplice programma per la conversione in HTML del file XML aderente alle specifiche tecniche
di `AVCP`__ in ottemperanza a Art.1,comma 32,L.190/2012 (anticorruzione).

Utilizzo
--------

:: 

  python avcpxml2html.py avcp_dataset_2013.xml

Produce (*forse*) il file avcp_dataset_2013.html

Il file XML in ingresso deve essere formalmente valido.
Un modo per validare il file XML in ingresso è fare uso del programma `xmllint`__ incluso nella libreria `libxml2`__::

  xmllint --noout --schema datasetAppaltiL190.xsd avcp_dataset_2013.xml
  avcp_dataset_2013.xml validates


Specifiche AVCP XML
-------------------

 * `Specifiche tecniche`__
 * `http://dati.avcp.it/schema/datasetAppaltiL190.xsd`__
 * `http://dati.avcp.it/schema/TypesL190.xsd`__


Note
~~~~

Tested with Python2.7 and Python3.3

:author: Michele Mordenti
:version: 0.3.1-dev
:license: GNU GPL v.3


__ http:/www.avcp.it
__ http://xmlsoft.org/xmllint.html
__ http://xmlsoft.org/
__ http://www.avcp.it/portal/rest/jcr/repository/collaboration/Digital%20Assets/pdf/AllCom27.05.13SpecificeTecnichev1.0.pdf
__ http://dati.avcp.it/schema/datasetAppaltiL190.xsd
__ http://dati.avcp.it/schema/TypesL190.xsd

