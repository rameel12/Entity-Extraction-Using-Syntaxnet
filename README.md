# Entity Extraction Using Syntaxnet



Entity Extraction is a subtask of [information extraction](https://en.wikipedia.org/wiki/Information_extraction) that seeks to locate and classify [named entities](https://en.wikipedia.org/wiki/Named_entity) in text into pre-defined categories such as the names of persons, organizations, locations, expressions of times, quantities, monetary values, percentages, etc.

NLP libraries like Spacy and NLTK are used for this purpose. The drawback is that any such libraries can get the common names and numbers but when used to find technical entities like &#39;Error message msg4567&#39; &#39;QUNTER\_ERROR\_IBM\_Server&#39; the built in functionalities in these libraries are not very useful.

To solve the issue we finalized dependency parsing method.A parse tree or parsing tree or derivation tree or concrete syntax tree is an ordered, rooted [tree](https://en.wikipedia.org/wiki/Tree_(data_structure)) that represents the [syntactic](https://en.wikipedia.org/wiki/Syntax) structure of a [string](https://en.wikipedia.org/wiki/String_(computer_science)) according to some [context-free grammar](https://en.wikipedia.org/wiki/Context-free_grammar).

NLP libraries like Spacy also provide functionality of creating and parsing dependency tree. Spacy &#39;Noun chunks&#39; function is able to extract the whole chunks of noun. In this case a lot of adjectives and verbs also become the part of the entity that, in our case, can be referred as garbage. The performance of spacy parsers was also bad when the sentences were complex and long. (Results are compared in the table below)

Syntaxnet is the best available tool for dependency parsing. It is the research of Google, open sourced, for better Natural Language Understanding. Its latest update took NLU to the next level, by understand long and complex commands and sentences.

Trees built by syntaxnet are more accurate and in more detail. After analysis, we decided to use these results and universal dependencies to find the required entities in our cases.

## Prerequisites 

Python 2.7 (Python 3. support is not available for Syntaxnet yet.)

Install [Syntaxnet](https://github.com/tensorflow/models/tree/master/research/syntaxnet)

Pandas

Numpy

## Syntaxnet Installation steps

Setting up Syntaxnet is a complicated task. There is a lot to do apart from what is mentioned in their wiki.

Following are the instructions to setup Syntaxnet on your machine

- Install python 2.7: (Can be installed separately or with anaconda)
- If tensorflow is installed, uninstall it:

-
  - _sudo pip uninstall tensorflow_
- Download **bazel 0.5.2**
- Run the following command:
  - _chmod +x bazel-0.5.2- installer…. (as per your file name).sh_
  - _./bazel(as per file name).sh –user_
  - _export PATH = &quot;$PATH:$HOME/bin&quot;_
- Check if bazel is installed:
  - _bazel version_
- Install Homebrew for IOS with the following command:
  - _/usr/bin/ruby -e &quot;$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)&quot;_
- Install swig
  - _brew install swig_ on OS(X)
- protocol buffers, with a version supported by TensorFlow:
  - _check your protobuf version with pip freeze | grep protobuf_
  - _upgrade to a supported version with pip install -U protobuf==3.3.0_
- autograd, with a version supported by TensorFlow:
  - _pip install -U autograd==1.1.13_
- mock, the testing package:
  - _pip install mock_
- asciitree, to draw parse trees on the console for the demo:
  - _pip install asciitree_
- numpy, package for scientific computing:
  - _pip install numpy_
- pygraphviz to visualize traces and parse trees:
  - _apt-get install -y graphviz libgraphviz-dev_
  - _pip install pygraphviz --install-option=&quot;--include-path=/usr/include/graphviz&quot; --install-option=&quot;--library-path=/usr/lib/graphviz/&quot;_
- Clone/Download the models library from github using the following command:
  - _git clone --recursive https://github.com/tensorflow/models.git_
- Version Compatibility is a huge issue in Syntaxnet Setup. Use the following commit id for bazel 0.5.2 to pass the bazel tests:
  - _Go to models forlder_
  - _git checkout _[_bc0edaf_](https://github.com/tensorflow/models/commit/bc0edaf8ec635c2a493a9303071e3d2fe97f3b7b)
  - _git submodule update_
  - _(commit id:bc0edaf8ec635c2a493a9303071e3d2fe97f3b7b)_
- Go to models/research/syntaxnet/tensorflow
- Run the following command:
  - _./configure_
- Come back to syntaxnet directory:
  - _cd .._
- Run the following commands for IOS:
  - _bazel_ _test_ _--linkopt=-headerpad\_max\_install\_names \dragnn/... syntaxnet/... util/utf8/..._
- Make a temporary directory:
  - _mkdir /tmp/syntaxnet\_pkg_
-  To install the tensorflow version compatible with the syntaxnet version you are installing, use the following command:
  -
    - _bazel-bin/dragnn/tools/build\_pip\_package --include-tensorflow –output-dir=/tmp/syntaxnet\_pkg__ _
- Install syntaxnet:
  - _sudo -H pip --no-cache-dir install /tmp/syntaxnet\_pkg/syntaxnet\_with\_tensorflow-0.2-whatever-your-config__uration-is.whl_
- Installation is done.


## Usage

```python
import entity_extractor as ep

s = ep.NER(" I work on 32 and 64 bit processor.")
print s #prints the list of entities
```



## Performance

Following are few results of Syntaxnet comparied with Spacy Noun Chunks

| **Text** | **Syntaxnet** | **Spacy** |
| --- | --- | --- |
| I work on **32 and 64 bit processor**. |32 bit processor,64 bit processor| I, 32 and 64 bit Processor|
| Update **IBM HTTP Server** for i to comply with **security vulnerabilities CVE-2011-0419** and **CVE-2011-1928** to maintain **PCI compliance**. |IBM HTTP Server,PCI compliance,security vulnerabilities CVE-2011-0419,security vulnerabilities CVE-2011-1928|Update IBM HTTP Server,I,security vulnerabilities,CVE-2011,CVE-2011,PCI compliance&#39;|
| An application using a Native **JDBC connections** is attempting to set the connection property for &quot; **server trace**&quot; to turn on job tracing. The **job trace** is not created and the joblog for the **QSQSRVR job** servicing the connection is logging an **error message msgMCH0801** and subsequently, **msgCPF3698** , **msgCPF4101** and **msgCPF9845.** This problem could also affect **SQL CLI trace functions**. |JDBC connections, QSQSRVR job, SQL CLI trace functions, Application, Connection,connection property, error message msgCPF3698, error message msgCPF4101, error message msgCPF9845, error message msgMCH0801, job trace, job tracing, joblog, problem, server trace| An application, a Native JDBC connections, the connection property, server trace, The job trace, the joblog, the QSQSRVR job, the connection, an error message msgMCH0801, subsequently, msgCPF3698, msgCPF9845, This problem, SQL CLI trace functions|
| The **Telnet Server attributes file** that has been upgraded from early **V3 Operating System** may contain BLANK values for **the VT100 Inbound and Outbound conversion files**. A recent **PTF** change to how those values are read will cause the **Telnet Server QTVTELNET job** to fail to start the **Telnet Server (23 or 992 Port) listener.** The **QTVTELNET job** will list a **MSGMCH3601 F/QTVTNCSH.** |values, VT100 Inbound conversion files, Telnet Server attributes file, V3 Operating System, VT100 Outbound conversion files, Telnet Server QTVTELNET job, PTF change, 23 Port, Telnet Server listener, values, 992 Port, MSGM CH 3601 F/QTVTNCSH, QTVTELNET job|The Telnet Server, file, early V3 Operating System, BLANK values, the VT100 Inbound and Outbound conversion files, A recent PTF change, those values, the Telnet Server QTVTELNET job, the Telnet Server, (23 or 992 Port, The QTVTELNET job, a MSGMCH3601 F/QTVTNCSH|
| An **MCH1210** is being signaled over **DRDA** for the **DESCRIBE of a TABLE** on a heterogeneous **application server** containing a **DecFloat field.** |DecFloat field, DESCRIBE, MCH1210, TABLE, application server, DRDA|An MCH1210, DRDA, the DESCRIBE,a TABLE,a heterogeneous application server, a DecFloat field|

The numbers are dealt ina way that they are only selected if they are a part of an entity.

For example:

&#39;_My age is 32 but I use 32 bit processor.&#39;_

The entities recognized by model using syntaxnet are &#39;age&#39; and &#39;32 bit processor&#39;

Similarly:

&#39;_VT100 Inbound and Outbound files&#39;_

The entities recognized by model are&#39; VT100 Outbound files. VT100 Inbound files.

As shown above, the accuracy of syntaxnet model seems to be above 90%.






**Syed Rameel Ahmad**

**Data Scientist IBM**
