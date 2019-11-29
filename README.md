# Entity Extraction Using Syntaxnet



Entity Extraction is a subtask of [information extraction](https://en.wikipedia.org/wiki/Information_extraction) that seeks to locate and classify [named entities](https://en.wikipedia.org/wiki/Named_entity) in text into pre-defined categories such as the names of persons, organizations, locations, expressions of times, quantities, monetary values, percentages, etc.

NLP libraries like Spacy and NLTK are used for this purpose. The drawback is that any such libraries can get the common names and numbers but when used to find technical entities like &#39;Error message msg4567&#39; &#39;QUNTER\_ERROR\_IBM\_Server&#39; the built in functionalities in these libraries are not very useful.

To solve the issue we finalized dependency parsing method.A parse tree or parsing tree or derivation tree or concrete syntax tree is an ordered, rooted [tree](https://en.wikipedia.org/wiki/Tree_(data_structure)) that represents the [syntactic](https://en.wikipedia.org/wiki/Syntax) structure of a [string](https://en.wikipedia.org/wiki/String_(computer_science)) according to some [context-free grammar](https://en.wikipedia.org/wiki/Context-free_grammar).

NLP libraries like Spacy also provide functionality of creating and parsing dependency tree. Spacy &#39;Noun chunks&#39; function is able to extract the whole chunks of noun. In this case a lot of adjectives and verbs also become the part of the entity that, in our case, can be referred as garbage. The performance of spacy parsers was also bad when the sentences were complex and long. (Results are compared in the table below)

Syntaxnet is the best available tool for dependency parsing. It is the research of Google, open sourced, for better Natural Language Understanding. Its latest update took NLU to the next level, by understand long and complex commands and sentences.

Trees built by syntaxnet are more accurate and in more detail. After analysis, we decided to use these results and universal dependencies to find the required entities in our cases.

After Data Analysis we built the following hypothesis:

- The label of a named entity will contain one of the following:
  -  &#39;sub&#39; (with an exception of csubj)&#39;,
  - &#39;ob&#39; (obl or obj) ,
  - appos (technical noun description of text, usually mentioned in speech marks or brackets)
  - nmod(Noun Modifier)
- All modifiers of these words are not required except:
  - Nummod(Numerical Modifier)
  - Flat (Noun, describing a noun)
  - Name (Name of a particular noun)
- Conjunctions will result in multiple entities.

Following are few results of Syntaxnet and Spacy

| **Text** | **Syntaxnet** | **Spacy** |
| --- | --- | --- |
| I work on **32 and 64 bit processor**. |32 bit processor,64 bit processor| I, 32 and 64 bit Processor|
| Update **IBM HTTP Server** for i to comply with **security vulnerabilities CVE-2011-0419** and **CVE-2011-1928** to maintain **PCI compliance**. |
- IBM HTTP Server
- PCI compliance
- security vulnerabilities CVE-2011-0419
- security vulnerabilities CVE-2011-1928
  |
- Update IBM HTTP Server
- I
- security vulnerabilities
- CVE-2011
- CVE-2011
- PCI compliance&#39;
  |
| An application using a Native **JDBC connections** is attempting to set the connection property for &quot; **server trace**&quot; to turn on job tracing. The **job trace** is not created and the joblog for the **QSQSRVR job** servicing the connection is logging an **error message msgMCH0801** and subsequently, **msgCPF3698** , **msgCPF4101** and **msgCPF9845.** This problem could also affect **SQL CLI trace functions**. |
- JDBC connections
- QSQSRVR job
- SQL CLI trace functions
- Application
- Connection
- connection property
- error message msgCPF3698
- error message msgCPF4101
- error message msgCPF9845
- error message msgMCH0801
- job trace
- job tracing
- joblog
- problem
- server trace
  |
- An application
- a Native JDBC connections
- the connection property
- server trace
- The job trace
- the joblog
- the QSQSRVR job
- the connection
- an error message msgMCH0801
- subsequently, msgCPF3698
- msgCPF9845
- This problem
- SQL CLI trace functions
  |
| The **Telnet Server attributes file** that has been upgraded from early **V3 Operating System** may contain BLANK values for **the VT100 Inbound and Outbound conversion files**. A recent **PTF** change to how those values are read will cause the **Telnet Server QTVTELNET job** to fail to start the **Telnet Server (23 or 992 Port) listener.** The **QTVTELNET job** will list a **MSGMCH3601 F/QTVTNCSH.** |
- values
- VT100 Inbound conversion files
- Telnet Server attributes file
- V3 Operating System
- VT100 Outbound conversion files
- Telnet Server QTVTELNET job
- PTF change
- 23 Port
- Telnet Server listener
- values
- 992 Port
- MSGM CH 3601 F/QTVTNCSH
- QTVTELNET job
  |
- The Telnet Server
- file
- early V3 Operating System
- BLANK values
- the VT100 Inbound and Outbound conversion files
- A recent PTF change
- those values
- the Telnet Server QTVTELNET job
- the Telnet Server
- (23 or 992 Port
- The QTVTELNET job
- a MSGMCH3601 F/QTVTNCSH
  |
| An **MCH1210** is being signaled over **DRDA** for the **DESCRIBE of a TABLE** on a heterogeneous **application server** containing a **DecFloat field.** |
- DecFloat field
- DESCRIBE
- MCH1210
- TABLE
- application server
- DRDA
  |
- An MCH1210
- DRDA
- the DESCRIBE
- a TABLE
- a heterogeneous application server
- a DecFloat field
  |

The numbers are dealt ina way that they are only selected if they are a part of an entity.

For example:

&#39;_My age is 32 but I use 32 bit processor.&#39;_

The entities recognized by model using syntaxnet are &#39;age&#39; and &#39;32 bit processor&#39;

Similarly:

&#39;_VT100 Inbound and Outbound files&#39;_

The entities recognized by model are&#39; VT100 Outbound files. VT100 Inbound files.

As shown above, the accuracy of syntaxnet model seems to be above 90%.



**Syed Rameel Ahmad**

**Data Scientist**
