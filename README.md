# **WoM Record Collection**
'WoM Record collection' is an application that helps you catalog your music collection. Examples of functions are *listing the collection*, *adding / changing / removing items*, *sorting the collection* and *calculating the total value of the collection*. The application targets users with an interest of collecting music that have a need of keeping track of their collection.

[View live website here](https://project-portfolio-3.herokuapp.com/)

![WoM responsive design](To be updated)

# Table of Content

* [**Project**](<#project>)
    * [Site Users Goal](<#site-users-goal>)
    * [Site Owners Goal](<#site-owners-goal>)

* [**User Experience (UX)**](<#user-experience-ux>)
    * [Flowchart](<#flowchart>)
    * [Wireframes](<#wireframes>)
    * [Site Structure](<#site-structure>)
    * [Design Choices](<#design-choices>)

* [**Features**](<#features>)
    * [Logo Area](<#logo-area>)
    * [Scoreboard Area](<#scoreboard-area>)
    * [Game Area](<#game-area>)
    * [Modals](<#modals>)

* [**Features Left To Implement**](<#features-left-to-implement>)

* [**Technologies Used**](<#technologies-used>)
    * [Languages](<#languages>)
    * [Frameworks, Librarys & Software](<#frameworks-libraries--software>)

* [**Testing**](<#testing>)
  * [Code Validation](<#code-validation>)
  * [Responsiveness Test](<#responsiveness-test>)
  * [Browser Compatibility](<#browser-compatibility>)
  * [Additional Testing](<#additional-testing>)
  * [Known Bugs](<#known-bugs>)
* [Deployment](<#deployment>)
* [Credits](<#credits>)
* [Acknowledgements](<#acknowledgements>)

#   Project

## **Site Users Goal**
To be updated

## **Site Owners Goal**
To be updated

[Back to top](<#table-of-content>)

# User Experience (UX)

## Flowchart
The flowchart for this application was made with the online service [Lucid App](https://lucid.app/).

![Flowchart](readme/assets/images/WoM_Record_Collection_Flowchart.png)

[Back to top](<#table-of-content>)

## Site Structure

## Design Choices

* ### Color Scheme

![Color Palette image](to be updated)

* ### Typography

[Back to top](<#table-of-content>)

# **Features**
To be updated

## **Existing Features**

* ### Welcome screen

 ![Welcome Screen](to be updated)

  * The welcome screen...

[Back to top](<#table-of-content>)


### Features Left to Implement

* To be updated


[Back to top](<#table-of-content>)

# Technologies Used

## Languages

* [Python](https://en.wikipedia.org/wiki/Python_(programming_language)) - provides the the functionality for the application.


## Frameworks, Libraries & Software

* [Github](https://github.com/) - used to host and edit the website.
* [Gitpod](https://www.gitpod.io/#get-started) - used to deploy the website.
* [Lighthouse](https://developer.chrome.com/docs/lighthouse/overview/) - used to test performance of site.
* [Responsive Design Checker](https://www.responsivedesignchecker.com/) - used for responsiveness check.
* [Wave Web Accessibility Evaluation Tool](https://wave.webaim.org/) - used to validate the sites accessibility.

[Back to top](<#table-of-content>)

# Testing

## Code Validation
To be updated...
  been tested through [W3C Markup Validaton Service](https://validator.w3.org/), [W3C CSS Validaton Service](https://jigsaw.w3.org/css-validator/) and [JSHint](https://jshint.com/). Errors were found on index.html in the W3C Markup Validaton Service but could quite easily be fixed (see [bugs section](#known-bugs)).

### Markup Validation
The Markup validator result, after fixing the minor errors can be seen below:

* Home Page

No errors were returned when passing through the official W3C validator.

![HTML Result Home Page](readme/assets/images/html_result_home_page.png)

[Back to top](<#table-of-content>)

### CSS Validaton
The CSS validator results can be seen below:

No errors were returned when passing through the official W3C validator.

![CSS Result](readme/assets/images/css_result.png)

[Back to top](<#table-of-content>)

### JSHint
The JSHint validator results can be seen below:

No errors were returned when passing through JSHint (*script.js*, *audio.js*, *modals.js*) but all tests reported issues connected to unused and undefined variables. These issues are not valid as the variables are used in other JavaScript files.

* script.js

![CSS Result](readme/assets/images/jshint_script.png)

* audio.js

![CSS Result](readme/assets/images/jshint_audio.png)

* modals.js

![CSS Result](readme/assets/images/jshint_modals.png)

[Back to top](<#table-of-content>)

# Responsiveness Test

The responsive design tests were carried out manually with [Google Chrome DevTools](https://developer.chrome.com/docs/devtools/) and [Responsive Design Checker](https://www.responsivedesignchecker.com/).

| Desktop    | Display <1280px       | Display >1280px    |
|------------|-----------------------|--------------------|
| Render     | pass                  | pass               |
| Images     | pass                  | pass               |
| Links      | pass                  | pass               |

| Tablet     | Samsung Galaxy Tab 10 | Amazon Kindle Fire | iPad Mini | iPad Pro |
|------------|-----------------------|--------------------|-----------|----------|
| Render     | pass                  | pass               | pass      | pass     |
| Images     | pass                  | pass               | pass      | pass     |
| Links      | pass                  | pass               | pass      | pass     |

| Phone      | Galaxy S5/S6/S7       | iPhone 6/7/8       | iPhone 12pro         |
|------------|-----------------------|--------------------|----------------------|
| Render     | pass                  | pass               | pass                 |
| Images.    | pass                  | pass               | pass                 |
| Links      | pass                  | pass               | pass                 |

*Comment: Scrolling is needed to some extent on some of the smaller screens*

[Back to top](<#table-of-content>)

## Browser Compatibility

'Memory of Queen Oblivion' was tested for responsiveness, functionality and appearance in the following browsers on desktop, tablet and phone with no visible issues for the user.

* Google Chrome Version (103.0.5060.114)
* Mozilla Firefox (version 102.0.1)
* Min (version 1.25.1)
* Apple Safari (version 15.5)
* Microsoft Edge (version 103.0.1264.62)

[Back to top](<#table-of-content>)

## Additional Testing

### WAVE

[WAVE](https://wave.webaim.org/) was used to check accessibility. 0 errors and 1 alerts was found. The alert was connected to page lacking a h1 (which is not a problem because the game has a headline image).

![WAVE Result](readme/assets/images/wave_result.png)

[Back to top](<#table-of-content>)

### Lighthouse
[Google Lighthouse](https://developers.google.com/web/tools/lighthouse) in Chrome Developer Tools was used to test the application within the areas of *Performance*, *Accessibility*, *Best Practices* and *SEO*. The testing showed that the *Accessability*, *Best Practices* and *SEO* was 100%. The Performance fluctuated between 75 and 90. To handle this I first compressed the *.png files and then also converted them to *.webp. After that I managed to squeeze the performance up to 88. I think the performance also is affected by the external scripts (connected to i.e. Bootstrap).

![Lighthouse Form Confirmation Page Result](readme/assets/images/lighthouse_result.png)

[Back to top](<#table-of-content>)

### Peer Review
Additional testing of the application was conducted by people outside of the software development field. Some spelling and grammar errors were found and corrected. No issues connected to gaming experience and visual design was reported. Template was used to control the different levels scenarios (see image below).

![Test Scenarios](readme/assets/images/level_scenarios.png)

## Known bugs

### Fixed Bugs

**2022-08-19**
* Bug: To be updated

![HTML Result Form Confirmation With Errors](to be updated)


### Unfixed Bugs

**2022-08-20**
* Bug: To be updated

![HTML Result Form Confirmation With Errors](to be updated)

[Back to top](<#table-of-content>)

# Deployment

## To Deploy The Project
The site was deployed to GitHub pages. The steps to deploy are as follows:

1. In the GitHub repository, navigate to the Settings tab

![Github Deploy Page 1](readme/assets/images/github_deploy_1.png)

[Back to top](<#table-of-content>)

2. Go to the Pages link in the left menu

![Github Deploy Page 2](readme/assets/images/github_deploy_2.png)

[Back to top](<#table-of-content>)

3. From the source section drop-down menu, select the main branch (can be master in some cases but for me it was main)

4. Once the main branch has been selected, the page will be automatically refreshed and information about successful deployment / publishing can be seen on screen. The live link can be found [here](https://worldofmarcus.github.io/project-portfolio-2/).

![Github Deploy Page 3](readme/assets/images/github_deploy_3.png)

[Back to top](<#table-of-content>)

## How To Fork The Repository On GitHub

It is possible to do a copy of a GitHub Repository by forking the GitHub account. The copy can then be viewed and it is also possible to do changes in the copy without affecting the original repository. To fork the repository, take these steps:

1. After logging in to GitHub, locate the repository. On the top right side of the page there is a 'Fork' button. Click on the button to create a copy of the original repository.

![Fork](readme/assets/images/github_fork.png)

[Back to top](<#table-of-content>)

## Create A Local Clone of A Project

To create a local clone of your repository, follow these steps:

1. When you are in the repository, find the code tab and click it.
2. To the left of the green GitPod button, press the 'code' menu. There you will find a link to the repository. Click on the clipboard icon to copy the URL.
3. Use an IDE and open Git Bash. Change directory to the location where you want the cloned directory to be made.
4. Type 'git clone', and then paste the URL that you copied from GitHub. Press enter and a local clone will be created.

![Clone](readme/assets/images/github_local_clone.png)

[Back to top](<#table-of-content>)

# Credits

## Content

* All text content written by Marcus Eriksson.

* All the icons on the website were taken from [Font Awesome](https://fontawesome.com/).

* [Template](https://github.com/Code-Institute-Solutions/readme-template) for read.me provided by Code Institute (*with some additional changes that my mentor [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/))* suggested.

## Technical

To be updated

* onLoad modal function taken from [Stack Overflow](https://stackoverflow.com/questions/10233550/launch-bootstrap-modal-on-page-load).


# Acknowledgements
The application 'WoM Record Collection' was completed as the Portfolio Project #2 (*JavaScript*) for the Full Stack Software Development Diploma at the [Code Institute](https://codeinstitute.net/). I would like to thank my mentor [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/) for relevant feedback during the project.

*Marcus Eriksson 2022-08-xx.*

[Back to top](<#table-of-content>)