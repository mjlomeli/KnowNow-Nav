# KnowNow-Nav
## Software 0.0.0.2

**Implementers** : Joshua Costa, Mauricio Lomeli, Hermain Hanif, Jennifer Kwon, Anne Wang, Dhruv Seth, 
Derek Eijansantos, Franny Chen, Meghna Islam

**Email** : [jshrager@stanford.edu](mailto:jshrager@stanford.edu) , 
[zhuo.rebecca@gmail.com](mailto:zhuo.rebecca@gmail.com), 
[smruti@gmail.com](mailto:smruti@gmail.com), [mjlomeli@uci.edu](mailto:mjlomeli@uci.edu)

Purpose

Currently we are working on *&quot;a sort of &#39;application oriented&#39; domain model. That is, there are, just as 
you have now, (diagnosis), symptoms, treatments, cohorts, and so on. There is discussion in the various forums about 
all of these… The graph (we) want, doesn&#39;t link domain entities to one another the way (we) have it now, but 
rather links these to posts (or threads) in the application model.&quot;* ~ Jeff Shrager

**New:** Documentation &amp; Author tags

- Everyone is required to credit themselves and others who have contributed to their code (ie professors and peers). 
Maintainer names come first before any other contributor in Author tag.
- Documentation is necessary for new recruits. Our program is getting too large for new recruits to make sense of it. We
 will have a very quick study on how to document. Each module will require some documentation by the end of the project.

Goals
-

##### Week 5: _Overview of our entire goals_

We will want to make our Neo4j driver as robust as we can with little to no errors. The natural language processor 
needs a way to subcategorize queries with tags, etc. The front-end needs to prepare for a search bar. Also, 
could improve the results page.

Have split the teams into 4 modules:

1. FileManager
   - Anyone new will begin here before transferring into something else.
   - Improve the file management and scheme of the spreadsheet using the Google drive provided spreadsheet.
   - Ideas: invoke a listener for changes in the Google drive to download new information when it is changed 
   (Anne had a good example, message her for details).
2. Neo4j
   - Need a robust way of creating nodes without failure and relations through matching already existing nodes.
   - Current pitfalls are creating duplicate nodes.
   - Thoroughly read Jeff&#39;s diagram and notes.
   - Ideas: Check before insertion if the node exists. Do we have all our required labels/properties prior to insertion?
3. Web
   - Needs to get connected to the front-end.
   - There is an additional link which needs to be added: [http://localhost:7474](http://localhost:7474) and 
   [https://localhost:7473](https://localhost:7473)
   - We need an error page connected for errors during the web navigation.
   - Prepare for a search bar.
   - Place try excepts linking to the error page.
   - Read up on uploading an AWS/GCP instance, we are going live.
   - We will be provided a real domain name and have a real website running.
4. NLP
   - Get the index structured based on the main category and subcategory.
   - Find and measure appropriate weights to each tag. Test, test, and test each weight among multiple queries 
and estimate if the result is correct.
5. Test
   - Each module will have its own tests.
   - The tests will test only the basics which is required (ie syntax, type conversions, None values, etc).


##### Week 6: _Likely to be updated closer to the start the week_

- Polish the Neo4j driver. Need to have the relationships just right.
- Be able to create a template for the Neo4j driver so that changes can occur without modifying the code.
- Web needs to have been connected. Currently should be working on the search bar and linking error pages to exceptions.
- Frontend needs to find an aesthetic way to introduce the new links [http://localhost:7474](http://localhost:7474) 
and [https://localhost:7473](https://localhost:7473) to open the Neo4j browser.
- Frontend could improve the error page to look nice.
- NLP should have the index built by now and started testing the weighing of each tag.
- Document one or two sections so you don&#39;t fall behind closer to the end of the project.

##### Week 7: _Likely to be updated closer to the start the week_

Combine the results within each group to scale up the application. Afterwards, provide details to the graphical user 
interface team for implementation.

- Web should have the search bar, error page, and Neo4j links connected. The next step is setting it live through 
GCP/AWS. Smruti will provide you with the domain, provide her with your public IP address to have it link directly 
to the instance.
- Web needs to learn about protocol and web security before making the final upload.
-  Neo4j team should have all node creation, deletion, and relations robust by now. The template design for insertion, 
deletion, and relations should be quite fair by now. The last goal is to be able to get information like a database. 
The next generation will very likely use this for scientific study.
- NLP team should be finished by now. I think its time to scale up to what we envisioned as a whole. Get your 
crawler to follow SEO principles prior to starting your massive crawl.
- Other NLP members, if you&#39;re using spaCy, we need you to extract from the original &#39;Insights&#39; 
spreadsheet and be able to have spaCy learn to make it more like the spreadsheet from &#39;Reconciled Insights&#39;. 
I&#39;m hoping SpaCy will link unstructured data with structured data and vice versa.

Week 8: _Likely to be updated closer to the start the week_

Sprint through and debug errors. We want to get as much code to work effectively. Any extra functionality which is not 
necessary will be marked as protected (do not remove). Then refractor so that no code that is dependent on it will 
raise an exception (ie test functions within the same file).

- Debugging
- Testing
- Deployment trials

### Approval of Minutes

**Team Meetings**

Every week there will be a When2Meet link posted on Slack on the #Software channel. Please provide your available 
times in which we can best accommodate our weekly meetings. These meetings are for you to provide us feedback with 
your ongoing progress and for us to collectively link our work. If any issues were to arise in your progress, 
you&#39;ll have the support of your team during these sessions.

**Advisory Meetings**

It&#39;s ideal to meet with an advisory committee after certain milestones have been completed. These meetings will 
be held on \[*dates to be completed*\] on weekly basis after \[*milestone name(s)*\] have been completed.

They will be scheduled preferably during the same day we have our team meetings. They are not mandatory but can 
provide you with a different insight from other professionals. We will schedule all meetings through Calendly or 
email with the appropriate advisor:

|   |   |   |
| --- | --- | --- |
| **Rebecca Zhuo** |   | [zhuo.rebecca@gmail.com](mailto:zhuo.rebecca@gmail.com) |
| **Smruti Vidwans** |   | [smruti@](mailto:smruti@gmail.com?subject=UCI::KnowNow%20Health%20-%20Volunteer)[gmail](mailto:smruti@gmail.com?subject=UCI::KnowNow%20Health%20-%20Volunteer)[.com](mailto:smruti@gmail.com?subject=UCI::KnowNow%20Health%20-%20Volunteer) |
| **Jeff Shrager** |   | [jshrager@stanford.edu](mailto:jshrager@stanford.edu) |

#### Advisory Committee

If you have any further questions beyond what Joshua or Mauricio can answer, please reach out to Rebecca Zhuo, 
Smruti Vidwans, or Jeff Shrager on Slack or email.

| [@Rebecca Zhuo](https://knownow-group.slack.com/team/UK1BN6EUT)  | [@Smruti Vidwns](https://knownow-group.slack.com/messages/DM6S2PNTS) | Jeff Shrager |
| --- | --- | --- |
| [zhuo.rebecca@gmail.com](mailto:zhuo.rebecca@gmail.com?subject=UCI::KnowNow%20Health%20-%20Volunteer)  | [smruti@gmail.com](mailto:smruti@gmail.com?subject=UCI::KnowNow%20Health%20-%20Volunteer) | [jshrager@stanford.edu](mailto:jshrager@stanford.edu) |

#### TimeBudget

Development is currently on a sprint. We have until the start of the Fall courses to deliver our second version. 
Around, Monday September 30th.



## Software 0.0.0.1
Our goal for this project is to create a prototype website/application search engine. 

**Implementers** : Joshua Costa, Mauricio Lomeli, Hermain Hanif, Shiyu Qiu, Jennifer Kwon, Anne Wang, Derek Eijansantos

**Email** : [mjlomeli@uci.edu](mailto:mjlomeli@uci.edu)

Purpose

&quot;Currently, we&#39;re working on the first part of the mission: to create and populate a knowledge base that 
defines patient cohorts and insights relevant to them by parsing &quot;open&quot; patient discussion forums.&quot; 
~ Rebecca Zhuo

Goals

  Week 1:

   Populate a knowledge base that _defines_ patient cohorts and insights relevant to them by parsing &quot;open&quot; 
   patient discussion forums.
   
   **Assignment Posted**: Google Drive/Shared with me/KnowNowVolunteer/#software/Week 1

   1. Select appropriate patient cohorts&#39; sites. Here are some examples:

      - [NCCN guidelines for breast cancer](https://knownow-group.slack.com/team/UK1BN6EUT)
      - [NCI](https://knownow-group.slack.com/team/UK1BN6EUT)
      - [FDA](https://open.fda.gov/)
      - [Oncotype DX](https://www.oncotypeiq.com/en-US/breast-cancer/healthcare-professionals/oncotype-dx-breast-recurrence-score/about-the-test)
      - [Lymph Node Status](https://ww5.komen.org/BreastCancer/LymphNodeStatusandStaging.html)
      - [Surgical margins and Guide to breast cancer pathology report](https://www.breastcancer.org/symptoms/diagnosis/margins)

   1. Web scrape and store the raw contents.
   2. Find a distributive mean of storing the data and outputting its raw results.

      - Find relationships and organization of the subject.
      - Select the appropriate database to deliver the results.
      - Organize and structure the nature of the contents.


  Week 2: _Likely to be updated closer to the start the week_

   - Find similarities among the content and relationships.
   - Classify cohort properties as tags with relevant patient insight.
   - Provide relevancy data in a manipulatable way.

  Week 3: _Likely to be updated closer to the start the week_

   Combine the results with data science group to define the application. Afterwards, provide details to the graphical 
   user interface team for implementation. Learn the patient&#39;s lifestyle and mold the design to fit their needs. 
  
   - Key important structure of the application: immediate results and as much decluttering as possible.
   - Schedule a meeting with the Data Science team and trade research.
   - Draw up designs and implementation GUI goals.
      1. Decide on the major tools required and prioritize them of importance.
      2. Test the application and debug

  Week 4: _Likely to be updated closer to the start the week_

Extra leeway for errors. In a project some extra room for errors is to be expected. This week will be for anything the 
rolls over before the deadline.

   - Debugging
   - Testing
   - Human Trials
   - Deployment

**Team Meetings**

Every week there will be a When2Meet link posted on Slack on the #Software channel. Please provide your available 
times in which we can best accommodate our weekly meetings. These meetings are for you to provide us with feedback 
with your ongoing progress and for us to collectively link our work with yours. If any issues were to arise in 
your progress, you&#39;ll have the support of your team during these sessions.

**Advisory Meetings**

It&#39;s ideal to meet with an advisory committee after certain milestones have been completed. These meetings 
will be held on a \[*daily/weekly*\] basis after \[*milestone name(s)*\] have been completed. They will be scheduled 
preferably during the same day we have our team meetings. They are not mandatory but can provide you with a different 
insight from other professionals. We will schedule all meetings through Calendly or email with the appropriate advisor:

|   |   |   |
| --- | --- | --- |
| **Rebecca Zhuo** |   | [rebeccazhuo/knownow-volunteer-onboarding](https://calendly.com/rebeccazhuo/knownow-volunteer-onboarding) |
| **Smruti Vidwans** |   | [smruti@gmail.com](mailto:smruti@gmail.com?subject=UCI::KnowNow%20Health%20-%20Volunteer) |

### TimeBudget

Development is currently on a sprint. We have until August 28 to deliver our final prototype.
