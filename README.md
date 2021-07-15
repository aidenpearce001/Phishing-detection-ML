# Phishing-detection-ML
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![Organization][organization-shield]][organization-url]
[![Organization][project-shield]][project-url]

<br />
<p align="center">
  <a href="https://github.com/aidenpearce001/Phishing-detection-ML">
    <img src="Images/logo.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Chongluadao</h3>

  <p align="center">
    [name] is a part of Project ChongLuaDao by using Model Deep Learning to detect the Phishing Website
    <br />
    <a href="http://103.90.227.67:45000/">View Demo</a>
    ·
    <a href="https://github.com/aidenpearce001/Phishing-detection-ML/issues">Report Bug</a>
    ·
    <a href="https://github.com/aidenpearce001/Phishing-detection-ML/issues">Request Feature</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
[![cld][cld-dashhboard]](https://example.com)

###About 
... is a part of Project ChongLuaDao by using Model **D**eep **L**earning to detect the Phishing Website
### Requirements

-   Python **3.7.x** | **3.8.x**

### Server tested on

-   Windows 10
-   Ubuntu 18.04

### Source for collecting data
#### Blacklist
- https://phishingreel.io/api/v1/panels/today
- https://api.chongluadao.vn/v1/blacklist
- http://data.phishtank.com/data/online-valid.csv (update every hour)
- https://raw.githubusercontent.com/mitchellkrogza/Phishing.Database/master/phishing-links/output/domains/ACTIVE/list (update every day)

#### Whitelist
- https://api.chongluadao.vn/v1/whitelist
- https://www.alexa.com/topsites/countries/VN
- https://webrank.vn/top-website-vietnam
- https://majestic.com/reports/majestic-million
- https://github.com/csirtgadgets/suspect-domains-dataset/blob/master/whitelist.txt

## Research (On going)
- https://www.academia.edu/10918579/A_WEB_CONTENT_ANALYTICS_ARCHITECTURE_FOR_MALICIOUS_JAVASCRIPT_DETECTION
- https://www.sciencedirect.com/science/article/pii/S1568494619305022
- https://www.just.edu.jo/~munzer/MyPubs/MALURLs_ITA2011.pdf
- https://www.researchgate.net/publication/228906286_Visual-Similarity-Based_Phishing_Detection
- https://www.mdpi.com/2073-8994/12/10/1681/pdf

## References
- http://docnum.univ-lorraine.fr/public/DDOC_T_2015_0058_MARCHAL.pdf
- https://research.aalto.fi/en/datasets/phishstorm-phishing-legitimate-url-dataset
- https://www.sciencedirect.com/science/article/pii/S1877050920310966
- https://www.atlantis-press.com/proceedings/iccsee-13/4487
- https://repository.asu.edu/attachments/189603/content/Namasivayam_asu_0010N_17146.pdf


[contributors-shield]:https://img.shields.io/badge/CONTRIBUTORS-5-green?style=for-the-badge
[contributors-url]: https://github.com/aidenpearce001/Phishing-detection-ML/graphs/contributors
[forks-shield]: https://img.shields.io/badge/FORKS-2-blue?style=for-the-badge
[forks-url]: https://github.com/aidenpearce001/Phishing-detection-ML/network/members
[stars-shield]: https://img.shields.io/badge/STARS-2-blue?style=for-the-badge
[stars-url]: https://github.com/aidenpearce001/Phishing-detection-ML/stargazers
[organization-shield]: https://img.shields.io/badge/organization-YoungIT-lightgrey?style=for-the-badge&logo=appveyor
[organization-url]: https://www.facebook.com/youngit.org
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[project-shield]: https://img.shields.io/badge/Project-chongluadao-green?style=for-the-badge&logo=appveyor
[project-url]: https://www.facebook.com/chongluadao.vn
[cld-dashhboard]: Images/dashboard.PNG
