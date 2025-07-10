## Resume Discipline Script - README
### First working prototype - Plan to add more customization so others can use it much more easily.

This is a Python program/script that centralizes multiple resumes in different disciplines. CS Majors apply to jobs in multiple disciplines at the same time and it can be a handful to manage and update all the resumes for each. A great way to fix this problem would be to update a single document containing all the sections for all disciplines and then creating document for each discipline. 

The idea came from a desire to improve my skills with LATEX. As a programmer, it would be more efficient to write in Latex with it's structured syntax and logical formatting system. Around the same time, I had a problem about having multiple resumes for different disciplines that I had to update. I was concerned about my resumes being inconsistent especially while applying for jobs. I realized I could solve my problem with LATEX. A document made up of code is much easier to read and write along with enforcing consistent formatting and templates as compared to a word processing program. The program would also be much simpler. 

Here is a simple rundown about how it works:

<ol>
  <li>The file "main.tex" is the "Master" resume with a simple resume format. It contains a section for education and experience that all the resumes share. It contains projects for all disciplines. It is to be edited in Overleaf and then downloaded in the same folder as "main.tex".</li>
  <li>Go through all of the lines and store then in a variable.</li>
  <li>We first have to go through "main.tex" and save all parts of the document that are part of the template and are shared between all of the resumes. Go through "main.tex" and store the line indexes for each line that contains "% TEMPLATE SECTION" via an array. Think of it as a section delimiter.</li>
  <li>We then go through the list and find the start and end of each section. We then go through all of the lines between the start and end and write them to a new file called "template.tex".</li>
  <li>We then have to specify the delimiters for each section and what files each delimiter refers to. This is done with two hashmaps.</li>
  <li>Find the start of the projects section with the delimiter "% PROJECTS - ".</li>
  <li>Go through each project section with a sliding window technique and write the projects to a new file for each discipline.</li>
  <li>Go through each "fullProjectFile.tex" file and store any lines with possible skills, including LANGUAGE, FRAMEWORK, TOOL, and LIBRARIES/APIS.</li>
  <li>Go through each of the files and write each section's skills.</li>
  <li>Write in the last 3 lines for the template to close the document.</li>
</ol>
