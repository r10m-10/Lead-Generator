CASE 1 -> user wants 3 businesses and there are no duplicate leads

found businesses = 4 (prev)

while loop condition = run till `count < n_leads`. This means that while loop should run till the number of businesses scraped is less than the number of leads the user wants.

entered the while loop

Iteration-1:
1. is `count < n_leads`? Yes, `count = 0` and `n_leads = 3`
2. is `count == prev`? No, `count = 0` and `prev = 4`. Thus, we skip loading new businesses.
3. `busi_idx = 0`. We look at the first business card and get its places id and do `busi_idx += 1`.
4. We check if the places id is already present in the database.
5. If it is already present then we have to do all the "changes" checks and if it isnt then we simply click on the card and collect other info and take it as a fresh lead and we do `count += 1`.
6. Since there are no duplicate leads, we simply take the business as a fresh lead and append it to `leads` in `results` dictionary.

Iteration-2:
1. is `count < n_leads`? Yes, `count = 1` and `n_leads = 3`
2. is `count == prev`? No, `count = 1` and `prev = 4`. Thus, we skip loading new businesses.
3. `busi_idx = 1`. We look at the second business card and get its places id and do `busi_idx += 1`.
4. We check if the places id is already present in the database.
5. If it is already present then we have to do all the "changes" checks and if it isnt then we simply click on the card and collect other info and take it as a fresh lead and we do `count += 1`.
6. Since there are no duplicate leads, we simply take the business as a fresh lead and append it to `leads` in `results` dictionary.

Iteration-3:
1. is `count < n_leads`? Yes, `count = 2` and `n_leads = 3`
2. is `count == prev`? No, `count = 2` and `prev = 4`. Thus, we skip loading new businesses.
3. `busi_idx = 2`. We look at the second business card and get its places id and do `busi_idx += 1`.
4. We check if the places id is already present in the database.
5. If it is already present then we have to do all the "changes" checks and if it isnt then we simply click on the card and collect other info and take it as a fresh lead and we do `count += 1`.
6. Since there are no duplicate leads, we simply take the business as a fresh lead and append it to `leads` in `results` dictionary.

Iteration-4:
1. is `count < n_leads`? No, `count = 3` and `n_leads = 3`

Exit while loop with 3 new leads generated.

Result: no time wasted on scrolling and finding new businesses and generated exactly 3 businesses.