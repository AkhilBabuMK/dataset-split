
# Split the database in training, testing and validation set

The **Vulnerability database generator** produces vulnerable and fixed synthetic samples expressing web vulnerability flaws.

This repository is the official implementation of this approach described in:

[Héloïse Maurel](https://dblp.uni-trier.de/search?q=heloise+maurel), [Santiago Vidal](https://sites.google.com/site/santiagoavidal/) and [Tamara Rezk](https://www-sop.inria.fr/everest/Tamara.Rezk/),
"Statically Identifying XSS using Deep Learning", SECRYPT 2021 [[PDF]](https://hal.inria.fr/hal-03684437)
_**April 2021** - The paper was accepted to [SECRYPT 2021](http://www.secrypt.org/?y=2021)_.
_**June 2022** - A journal version was accepted to [Science of Computer Programming, Volume 219](https://www.sciencedirect.com/science/article/abs/pii/S0167642322000430)_.

## Citations

**Statically identifying XSS using deep learning**, [Héloïse Maurel](https://gitlab.inria.fr/deep-learning-applied-on-web-and-iot-security/), [Santiago Vidal](https://sites.google.com/site/santiagoavidal/) and [Tamara Rezk](https://www-sop.inria.fr/everest/Tamara.Rezk/), In Proceedings of [Science of Computer Programming, Volume 219](https://www.sciencedirect.com/science/article/abs/pii/S0167642322000430), 2022
- Online at hal.inria : [PDF](https://hal.inria.fr/hal-03684437)
- Citation in .bibTex format :

		   @article{DBLP:journals/scp/MaurelVR22,
		     author    = {H{\'{e}}lo{\"{\i}}se Maurel and
		                  Santiago A. Vidal and
		                  Tamara Rezk},
		     title     = {Statically identifying {XSS} using deep learning},
		     journal   = {Sci. Comput. Program.},
		     volume    = {219},
		     pages     = {102810},
		     year      = {2022},
		     url       = {https://doi.org/10.1016/j.scico.2022.102810},
		     doi       = {10.1016/j.scico.2022.102810},
		     timestamp = {Wed, 01 Jun 2022 15:34:38 +0200},
		     biburl    = {https://dblp.org/rec/journals/scp/MaurelVR22.bib},
		     bibsource = {dblp computer science bibliography, https://dblp.org}
		   }

**Statically identifying XSS using deep learning**, [Héloïse Maurel](https://gitlab.inria.fr/deep-learning-applied-on-web-and-iot-security/), [Santiago Vidal](https://sites.google.com/site/santiagoavidal/) and [Tamara Rezk](https://www-sop.inria.fr/everest/Tamara.Rezk/), In Proceedings of [SECRYPT 2021](https://secrypt.scitevents.org/Home.aspx?y=2021)

- Online at hal.inria : [PDF](https://hal.inria.fr/hal-03273564)
- Citation in .bibTex format :

            @inproceedings{DBLP:conf/secrypt/MaurelVR21,
			  author    = {H{\'{e}}lo{\"{\i}}se Maurel and
			               Santiago A. Vidal and
			               Tamara Rezk},
			  editor    = {Sabrina De Capitani di Vimercati and
			               Pierangela Samarati},
			  title     = {Statically Identifying {XSS} using Deep Learning},
			  booktitle = {Proceedings of the 18th International Conference on Security and Cryptography,
			               {SECRYPT} 2021, July 6-8, 2021},
			  pages     = {99--110},
			  publisher = {{SCITEPRESS}},
			  year      = {2021},
			  url       = {https://doi.org/10.5220/0010537000990110},
			  doi       = {10.5220/0010537000990110},
			  timestamp = {Wed, 16 Mar 2022 10:02:02 +0100},
			  biburl    = {https://dblp.org/rec/conf/secrypt/MaurelVR21.bib},
			  bibsource = {dblp computer science bibliography, https://dblp.org}
			}




## Overview
One of the essential steps to apply any supervised deep learning algorithm is to design a reliable and comprehensive dataset. 
In our case, the server-side code cannot be obtained by browsing the web, and it is difficult to reliably and automatically classify the server-side code on public repositories, like XSS-safe or unsafe. Thus, we explore the use of a synthetic
generator of vulnerabilities for XSS flaws.

## Prerequisites

* Linux (developed on Ubuntu and Fedora)
* Python >= 3.3.3 (developed on 3.9)

A [Python](https://www.python.org/downloads/) installation is needed to run the generator.

This repository contains the main script to split the database generate by the generator of this project into 3 datasets :
- training
- testing
- validation

The database generate by the generator will have this kind of structure folder :
- database
    - xss
        - safe
        - unsafe

Give only the subfolder `xss` with these children folders.

In this end, you will obtain a new database such as :
- trainset_files
    - safe
    - unsafe
- testset_files
    - safe
    - unsafe
- validationset_files
    - safe
    - unsafe

