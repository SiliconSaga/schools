# Filing the requests: October 14, 2026

One copy of the steps for all three requests. The request texts are in `_includes/opra/`; the printable letters come from `tools/opra-print.py`. Not legal advice.

## Before you leave

1. Fill in `requester.yml` (copy `requester.example.yml`; the real file is ignored by git because it carries a phone number). Name, street address, email, and phone all matter: a requester who leaves them off cannot challenge a denial, and silence from the district is then not a deemed denial.
2. Pick the email address you will put on the letters and watch it for the next month. It is where the district will reply, and the deadline is counted whether or not anyone reads the inbox. If you use an alias such as schools@frontstate.org, send yourself a test message first.
3. Render the letters: `ws exec schools python _research/tools/opra-print.py` writes `_research/opra/out/OPRA-00N-....pdf` for each request (the folder is ignored by git). Open each PDF and read it once as the custodian would.
4. Print two copies of each letter, six in all, and six copies of the district's form, `../sources/opra-form.pdf` (the district page at https://www.woboe.org/departments/business-office/opra-request offers the form, the address 179 Eagle Rock Ave., and the phone 973-669-5400, and names no custodian or email). Fill in each form by hand, write "See attached, OPRA-00N" in the records box, and staple the matching letter behind it. One stapled set of each request is handed in; the other comes back stamped.

## At the Business Office, 179 Eagle Rock Avenue

1. Ask who the custodian of records is and write the name down. The district site still lists Tonya Flowers as Business Administrator/Board Secretary; the July 21 minutes authorize Trenae Lambkin to award contracts from May 25, 2026, and a July news report has her as acting business administrator and board secretary.
2. Hand over one copy of each request. Ask for the second copy to be date-stamped "received" and handed back, or for a signed and dated receipt. Photograph the stamped copies before you leave.
3. Ask which email address OPRA requests and responses go to, and whether the EduStaff agreement (a contract less than 24 months old, immediate access under 47:1A-5(e)) can be emailed that day. Expect to be told it will follow.

## From the lobby, or as soon as you are home

Send one email per request to the address they gave you, from the address on the letters, with the PDF attached. Suggested text, with the subject line matching the letter:

> Subject: OPRA request: Paraprofessional staffing contract and billing (requester reference OPRA-001), hand-delivered October 14, 2026

The "requester reference" is this ledger's own numbering, not the district's; it is on the letter so that each response can be matched to its request.
>
> Dear Custodian of Records,
>
> Attached is the request I hand-delivered to the Business Office today, October 14, 2026, with the district's OPRA form. I am sending the same text by email so that you have an electronic copy and so that the records can be sent to this address. Please confirm receipt.
>
> Thank you,
> Rasmus Praestholm
> [street address]
> [phone]

Note the time each email was sent. The stamped copy and the sent email are the two receipts the ledger publishes, with the street address and phone number removed.

## The clock

Business days are counted from the day after receipt, Wednesday, October 14, 2026, and exclude weekends and legal holidays.

- **Seven business days:** Thursday the 15th, Friday the 16th, then Monday the 19th through Friday the 23rd. The district must grant, deny, or say in writing that the records are in storage, by **Friday, October 23, 2026**. Silence past that date is a deemed denial.
- **Fourteen business days** (only if the district treats a request as needing Daniel's Law review): Monday the 26th through Friday the 30th, then Monday, November 2 and Tuesday, November 3. Tuesday, **November 3, 2026** is General Election Day, a state legal holiday; if the district office is closed that day the date moves to Wednesday, November 4. Check the district calendar before logging it.
- A denial, including a deemed denial, can be challenged within 45 days at the Government Records Council or in Superior Court.

## After filing: what to change in the repository

1. `_data/opra.yml`: for each request, `status: filed`, `filed: 2026-10-14`, `due: 2026-10-23`.
2. `ledger/opra/00N-*.md`: add a Log line, "**October 14, 2026.** Hand-delivered to the Business Office at [time] and emailed to [address] at [time]. Receipt stamped." Name the custodian if one was given.
3. Save the stamped receipts, with address and phone redacted, as `../sources/opra-00N-receipt-2026-10-14.pdf`, and list each under `documents:` in `opra.yml` once the files are also placed where the site can serve them (a `ledger/opra/files/` folder, to be created with the first document).
4. Add a timeline entry dated 2026-10-14, basis `record`, "Three public-records requests filed", sourced to the receipts.
5. Every response from the district, in full, goes the same way: saved copy, `documents:` entry, Log line, and a status change (`partial`, `fulfilled`, `denied`, or `overdue` on October 26 if nothing has arrived).
