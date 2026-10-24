# FRONTEND DECISIONS

1. Signup will have 4 pages:
    - PAGE-1: ask for name, email and password. Call `/users/check-email` endpoint.
    - PAGE-2: ask for username. Call `users/check-username` endpoint.
    - PAGE-3: ask for signup type - Business/Indivisual
    - PAGE-4: ask for team name if signup type is business. Finally, single API call to `/users` to create the user.

2. Auth token storage: JWT will be stored in httpOnly cookies and not in localStorage.

3. Leads Dashboard will have 2 sections:
    - New Leads: Freshly generated leads.
    - Duplicate leads: these are the leads that already exist on the database. These leads have specific codes to signify what type of duplicate are they. The codes are:-

        `0 = new name and website` \| `1 = new name, same website` \| `2 = same name, new website` \| `3 = complete duplicate`
     
        These number codes also signify the priority order in which these duplicate leads should be displayed in the frontend - 0 being the highest and 3 being the lowest.

4. In the "Duplicate leads" section, the user also has the option to reinstate specific (or all) leads. Reinstating means clearing a fag code and treating it as a fresh lead that must be acted upon.

5. Use this website to learn various stuff about UI/UX design: https://www.iamsajid.com/

6. Use a "website color palette generator" to get some color Ideas.

7. In the onboarding steps (PAGE-2 signup), I am thinking of some cool arrow animation. I am thinking that when the user enters their username and clicks on the button, the arrow grows and then reveals the next page Under it.

8. while generating leads, the user will see 2 options. In the first one, the user will be asked to enter their query. In the second one, the user will be asked to add an upper limit to their search.

9. There will also be a "+" button at the bottom of each "query box" of "query batch" so that a user can add another query box and mix and match how many leads they want and what queries they want. both questions are required for a query and hence there will be a continue button only when both a re filled. If the user adds a new box then the continue button will again disappear until both of the new questions are filled and so on and so forth.

10. We need a new "Manage Leads" tab where the user can do all sorts of stuff with their leads like view generation history, view all batches, push generated batches to the team, remove batches, break up batches, set deadline on batches, etc.

11. The manage leads tab will query the "/batches" endpoint to list all the batches chronologically. The batches will be like a rectangular card and will show the query that generated that batch. Then, the user can click on any batch to view all the leads generated inside that batch. There, the user can also find all the batch management settings such as publish batch, delete batch, break batch, set deadline and other (TBD) batch related functions. Also, duplicate leads will be handled as follows:
Generate 10 leads -> 5 duplicate leads -> show popup saying "this query generated some duplicate leads, check out the flagged batches" -> user goes back to the manage leads tab and checks out all the batches with the duplicate leads -> user will be able to reinstate required leads and extend deadline if required.
**NOTE:** Reinstating lead will make it pop up straight back up on the employee table as a fresh lead.
Also, batches cannot be un-published.