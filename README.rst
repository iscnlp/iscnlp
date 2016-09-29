iscnlp
======

|travis| |CircleCI| |coverage|

----

Natural Language tool-kit for Indian languages

Install dependencies
^^^^^^^^^^^^^^^^^^^^

::

    pip install -r requirements.txt

Before Install
^^^^^^^^^^^^^^

`iscnlp <https://github.com/iscnlp/iscnlp>`_ contains large files which are managed through `git-lfs`_. Git-Lfs replaces large files with text pointers inside Git, while storing the file contents on a remote server. To convert these text pointers back to actual files `git-lfs`_ should be installed. Run the below commands to install `git-lfs`_.

.. _`git-lfs`: https://git-lfs.github.com

::

    - curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
    - sudo apt-get install git-lfs

Install
^^^^^^^

::

    - git clone https://github.com/iscnlp/iscnlp.git
    - cd iscnlp
    - git lfs install
    - git lfs pull
    - sudo python setup.py install

1. Tokenizer:
-------------

.. code:: python

    >>> from __future__ import unicode_literals
    >>> from iscnlp import Tokenizer
    >>> tk = Tokenizer(lang='hin')
    >>> tk.tokenize("22 साल के लंबे इंतजार के बाद आखिरकार हॉलीवुड स्टार लियोनार्डो डिकैप्रियो को अपनी पहली ऑस्कर ट्रॉफी"
    ...             " मिल चुकी है। उन्हें ये अवॉर्ड अपनी फिल्म ‘द रेवेनेंट’ में ह्यूज ग्लास के किरदार के लिए मिला, लेकिन उनके"
    ...             " के लिए रोल निभाना आसान नहीं था।")
    ['22', 'साल', 'के', 'लंबे', 'इंतजार', 'के', 'बाद', 'आखिरकार', 'हॉलीवुड', 'स्टार', 'लियोनार्डो', 'डिकैप्रियो', 'को', 'अपनी', 'पहली', 'ऑस्कर', 'ट्रॉफी', 'मिल', 'चुकी', 'है', '।', 'उन्हें', 'ये', 'अवॉर्ड', 'अपनी', 'फिल्म', "'", 'द', 'रेवेनेंट', "'", 'में', 'ह्यूज', 'ग्लास', 'के', 'किरदार', 'के', 'लिए', 'मिला', ',', 'लेकिन', 'उनके', 'के', 'लिए', 'रोल', 'निभाना', 'आसान', 'नहीं', 'था', '।']
    >>> tk = Tokenizer(lang='hin', split_sen=True)
    >>> tk.tokenize("22 साल के लंबे इंतजार के बाद आखिरकार हॉलीवुड स्टार लियोनार्डो डिकैप्रियो को अपनी पहली ऑस्कर ट्रॉफी"
    ...             " मिल चुकी है। उन्हें ये अवॉर्ड अपनी फिल्म ‘द रेवेनेंट’ में ह्यूज ग्लास के किरदार के लिए मिला, लेकिन उनके"
    ...             " के लिए रोल निभाना आसान नहीं था। फिल्म एक सीन के लिए लियोनार्डो को भैंस का कच्चा लीवर खाना"
    ...             " पड़ा था। जबकि असल जिंदगी में वो पूरी तरह शाकाहारी हैं। हालांकि इस सीन के लिए पहले लियोनार्डो को"
    ...             " मांस जैसे दिखने वाली चीज दी गई थी, लेकिन उन्हें लगा कि ऐसा करना गलत होगा। फिल्म के लिए इम्पोर्ट"
    ...             " की गई चीटियां...")
    [['22', 'साल', 'के', 'लंबे', 'इंतजार', 'के', 'बाद', 'आखिरकार', 'हॉलीवुड', 'स्टार', 'लियोनार्डो', 'डिकैप्रियो', 'को', 'अपनी', 'पहली', 'ऑस्कर', 'ट्रॉफी', 'मिल', 'चुकी', 'है', '।'], ['उन्हें', 'ये', 'अवॉर्ड', 'अपनी', 'फिल्म', "'", 'द', 'रेवेनेंट', "'", 'में', 'ह्यूज', 'ग्लास', 'के', 'किरदार', 'के', 'लिए', 'मिला', ',', 'लेकिन', 'उनके', 'के', 'लिए', 'रोल', 'निभाना', 'आसान', 'नहीं', 'था', '।'], ['फिल्म', 'एक', 'सीन', 'के', 'लिए', 'लियोनार्डो', 'को', 'भैंस', 'का', 'कच्चा', 'लीवर', 'खाना', 'पड़ा', 'था', '।'], ['जबकि', 'असल', 'जिंदगी', 'में', 'वो', 'पूरी', 'तरह', 'शाकाहारी', 'हैं', '।'], ['हालांकि', 'इस', 'सीन', 'के', 'लिए', 'पहले', 'लियोनार्डो', 'को', 'मांस', 'जैसे', 'दिखने', 'वाली', 'चीज', 'दी', 'गई', 'थी', ',', 'लेकिन', 'उन्हें', 'लगा', 'कि', 'ऐसा', 'करना', 'गलत', 'होगा', '।'], ['फिल्म', 'के', 'लिए', 'इम्पोर्ट', 'की', 'गई', 'चीटियां', '...']]

Tokenizer can also be called from Command Line Interface.

.. parsed-literal::

    irshad@iscnlp$ isc-tokenizer --h
    usage: Indic-Tokenizer [-h] [-v] [-i] [-s] [-o] [-l]
    
    Tokenizer for Indian Scripts
    
    optional arguments:
      -h, --help              show this help message and exit
      -v, --version           show program's version number and exit
      -i , --input            <input-file>
      -s, --split-sentences   set this flag to apply sentence segmentation
      -o , --output           <output-file>
      -l , --language         select language (3 letter ISO-639 code) {hin, urd,
                              ben, asm, guj, mal, pan, tel, tam, kan, ori, mar, nep,
                              bod, kok, kas, eng}


2. POS-Tagger
-------------

.. code:: python

    >>> from __future__ import unicode_literals
    >>> from iscnlp import Tagger
    >>> from iscnlp import Tokenizer
    >>> tk = Tokenizer(lang='hin')
    >>> tagger = Tagger(lang='hin')
    >>> sequence = tk.tokenize("केजरीवाल पर प्रहार करते हुए अखिलेश ने कहा कि जब तक पूरे मामले की जांच रिपोर्ट जनता के"
    ...                        " सामने नहीं आ जाती, कोई कैसे कह सकता है कि जांच निष्पक्ष है या नहीं।")
    >>> sequence
    ['केजरीवाल', 'पर', 'प्रहार', 'करते', 'हुए', 'अखिलेश', 'ने', 'कहा', 'कि', 'जब', 'तक', 'पूरे', 'मामले', 'की', 'जांच', 'रिपोर्ट', 'जनता', 'के', 'सामने', 'नहीं', 'आ', 'जाती', ',', 'कोई', 'कैसे', 'कह', 'सकता', 'है', 'कि', 'जांच', 'निष्पक्ष', 'है', 'या', 'नहीं', '।']
    >>> tagger.tag(sequence)
    [('केजरीवाल', 'NNP'), ('पर', 'PSP'), ('प्रहार', 'NN'), ('करते', 'VM'), ('हुए', 'VAUX'), ('अखिलेश', 'NNP'), ('ने', 'PSP'), ('कहा', 'VM'), ('कि', 'CC'), ('जब', 'PRP'), ('तक', 'PSP'), ('पूरे', 'JJ'), ('मामले', 'NN'), ('की', 'PSP'), ('जांच', 'NNC'), ('रिपोर्ट', 'NN'), ('जनता', 'NN'), ('के', 'PSP'), ('सामने', 'NST'), ('नहीं', 'NEG'), ('आ', 'VM'), ('जाती', 'VAUX'), (',', 'SYM'), ('कोई', 'PRP'), ('कैसे', 'WQ'), ('कह', 'VM'), ('सकता', 'VAUX'), ('है', 'VAUX'), ('कि', 'CC'), ('जांच', 'NN'), ('निष्पक्ष', 'JJ'), ('है', 'VM'), ('या', 'CC'), ('नहीं', 'NEG'), ('।', 'SYM')]

POS text files directly from Command Line Interface. It is highly recommended to tokenize the text files before POS-tagging.

.. parsed-literal::

    irshad@iscnlp$ isc-tagger --h
    usage: isc-tagger [-h] [-v] [-i] [-o] [-l]
    
    POS-Tagger for Indian Languages
    
    optional arguments:
      -h, --help        show this help message and exit
      -v, --version     show program's version number and exit
      -i , --input      <input-file>
      -o , --output     <output-file>
      -l , --language   select language (3 letter ISO-639 code) {hin, urd}

3. Parser
---------

.. code:: python

    >>> from iscnlp import Parser
    >>> parser = Parser(lang='hin')
    >>> text = "यदि आप इस उक्ति पर विश्वास करते हैं तो कोस्टर डायमंड का चक्कर जरूर लगाइएगा ."
    >>> text = text.split()
    >>> text
    ['यदि', 'आप', 'इस', 'उक्ति', 'पर', 'विश्वास', 'करते', 'हैं', 'तो', 'कोस्टर', 'डायमंड', 'का', 'चक्कर', 'जरूर', 'लगाइएगा', '.']
    >>> tree = parser.parse(text)
    >>> print('\n'.join(['\t'.join(node) for node in tree]))
    1	यदि	यदि	CC	CC	_	9	vmod	_	_
    2	आप	आप	PRP	PRP	_	7	k1	_	_
    3	इस	इस	DEM	DEM	_	4	nmod__adj	_	_
    4	उक्ति	उक्ति	NN	NN	_	7	k7	_	_
    5	पर	पर	PSP	PSP	_	4	lwg__psp	_	_
    6	विश्वास	विश्वास	NN	NN	_	7	pof	_	_
    7	करते	करते	VM	VM	_	1	ccof	_	_
    8	हैं	हैं	VAUX	VAUX	_	7	lwg__vaux	_	_
    9	तो	तो	CC	CC	_	0	main	_	_
    10	कोस्टर	कोस्टर	NNPC	NNPC	_	11	pof__cn	_	_
    11	डायमंड	डायमंड	NNP	NNP	_	13	r6	_	_
    12	का	का	PSP	PSP	_	11	lwg__psp	_	_
    13	चक्कर	चक्कर	NN	NN	_	15	k1	_	_
    14	जरूर	जरूर	RB	RB	_	15	adv	_	_
    15	लगाइएगा	लगाइएगा	VM	VM	_	9	ccof	_	_
    16	.	.	SYM	SYM	_	9	rsym	_	_

Parse raw-text files directly from Command Line Interface. It is highly recommended to tokenize the text files before parsing.

.. parsed-literal::

    irshad@iscnlp$ isc-parser --h
    usage: isc-parser [-h] [-v] [-i] [-o] [-l]
    
    Parser for Indian Languages
    
    optional arguments:
      -h, --help        show this help message and exit
      -v, --version     show program's version number and exit
      -i , --input      <input-file>
      -o , --output     <output-file>
      -l , --language   select language (3 letter ISO-639 code) {hin, urd}

----

|travis| |CircleCI| |coverage|

.. |travis| image:: https://travis-ci.org/iscnlp/iscnlp.svg?branch=master
   :target: https://travis-ci.org/iscnlp/iscnlp
   :alt: travis-ci build status

.. |CircleCI| image:: https://circleci.com/gh/iscnlp/iscnlp.svg?style=svg
    :target: https://circleci.com/gh/iscnlp/iscnlp

.. |coverage| image:: https://coveralls.io/repos/github/iscnlp/iscnlp/badge.svg?branch=master 
   :target: https://coveralls.io/github/iscnlp/iscnlp?branch=master
   :alt: coveralls.io coverage status
