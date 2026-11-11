# Experiments register

Status: running, candidate, confirmed, fluke, retired, tired. Lift = impressions / channel 28-day median.
Rules: tools/social-cards/TEST-AND-LEARN.md.

## Baselines at 01/11/2026 (28-day medians, posts older than 48 hours)

- Presso page: 36 impressions per post
- Corey page: 4 impressions per post (channel problem: audience too small to read much from yet)
- Kristian: 139 impressions per post

## Candidates carried in (lift >= 2 before this register existed)

| id | channel | what won | lift | status | replicate by |
|---|---|---|---|---|---|
| C-01 | Corey | before/after on a real bug with the exact error string ("Same error. Two habits.", 28/10) | 66 / 4 = 16.5 | candidate | Corey Thu 05/11 flow on the same blog's three exit codes (same "real bug, exact output" angle, new layout) |
| C-02 | Presso | a hard £ worked example in an infographic, evening (Eventbrite fees, 04/10 22:02) | 299 / 36 = 8.3 | candidate | Presso Wed 04/11 20:30 numbers infographic (hard numbers, evening slot) |
| C-03 | Kristian | a real event, real people, a photo (Digital Masters panel, 20/10) | 619 / 139 = 4.5 | candidate | only when Kristian does another public event (we never invent one) |
| C-04 | Kristian | MCP explained as a diagram infographic (04/10, 296) | 296 / 139 = 2.1 | candidate | Presso Fri 06/11 "Where MCP sits" hub (same idea, brand page, new layout) |

## Experiments running, week 45 (02/11 to 07/11/2026)

| id | channel | hypothesis | change | posts | status |
|---|---|---|---|---|---|
| E-01 | Presso, Corey | Diagrams with connector lines (hub, flow) beat lists and cards | layout | PE Thu hotels hub, PE Fri MCP hub, PE Sat flow; CO Tue cuban hub, CO Thu flow; KP Mon flow | running |
| E-02 | Presso, Corey | Trending-topic posts beat evergreen posts | topic source | PE Tue agents, PE Thu hotels; CO Tue Cuban, CO Sat AI slop | running |
| E-03 | Presso, Corey | 20:30 beats the main slot | time | PE Wed, PE Sat; CO Tue, CO Thu | running |
| E-04 | Presso | Percentages on a 0-100% scale beat bare big numbers | bars vs stats | PE Tue bars vs PE Wed stats | running |
| E-05 | Corey | An AI admitting its own awkward position draws comments ("I'm an AI. I'd flag me too.") | hook type: self-deprecating confession | CO Sat 07/11 | running (explore) |

## Run of Wed 04/11/2026: week 46 posts Mon 09/11 to Wed 11/11 (Presso, Corey)

Mature results this run: no candidate added (no new post with lift >= 2; the three highest are older). E-01 to E-05 stay running; their week-45 posts are mostly under 48 hours old. First mature IG-look posts: PE 02/11 lift 1.09, CO 02/11 lift 0.5, KP 02/11 lift 1.21 (n=3, no conclusion).

| id | channel | hypothesis | change | posts | status |
|---|---|---|---|---|---|
| E-06 | Presso | CMO D-4: 09:00 beats 10:00 | time (09:00 vs 10:00) | PE Tue 10/11 09:00 (EDR versus, trending, explore) | running |
| E-07 | Corey | A test slot of 08:00 does not lose to 09:20 | time | CO Tue 10/11 08:00 (success versus, evergreen, C-01 replication) | running |
| E-08 | Presso, Corey | Trending posts with hard sourced numbers beat evergreen (D-9) | topic source | trending: PE Mon, PE Tue, CO Mon, CO Wed. evergreen: PE Wed, CO Tue | running |
| E-09 | Presso | A studio incident told as a flow with exact tokens (586,000 vs 200,000) beats a definition | hook: hard number from our own build | PE Wed 11/11 10:00 (tracked link: "tracked link" experiment, compare with the same format without a link) | running (replicates C-02) |

Candidate replications scheduled: C-01 (Corey, real incident, exact counts: 25 mornings, "queued" count) as CO Tue 10/11 08:00 in the versus layout (new layout, new text, new slot). C-02 (Presso, hard numbers) as PE Mon 09/11 hub (98%, 17.3M) and PE Wed 11/11 flow (586k vs 200k). C-04 (MCP idea in a diagram): PE Mon hub. C-03 (Kristian, real event): not replicable, no new event.
Exploit / refine / explore this run: PE Mon exploit (C-02/C-04), PE Tue explore (new layout on trending security angle, CMO slot), PE Wed exploit+tracked link; CO Mon refine (hub, trending, self-deprecating hook), CO Tue exploit (C-01), CO Wed refine (flow story, first-person confession).

## Run of Fri 06/11/2026: week 46 posts Thu 12/11 and Fri 13/11 (Presso, Corey)

Mature results: no new candidate. C-01 replication (CO Thu 05/11 20:30, three-states flow) is at 10 impressions (lift 2.5) but only 36 hours old: confirm or flag as fluke in the next file. C-02 replication (PE Wed 04/11 20:30 numbers) at 30 (lift 1.30), young. KP 04/11 text post (593, lift 3.8) is NOT logged as a candidate: it breaks the profile HARD BLOCK. E-01 to E-09 remain running; mature IG n is 5 (PE 38, 6; CO 3, 4; KP 225), no conclusion.

| id | channel | hypothesis | change | posts | status |
|---|---|---|---|---|---|
| E-08 (cont.) | Presso, Corey | Trending posts with hard sourced numbers beat evergreen | topic source | trending: PE Thu 12/11 (bars), PE Fri 13/11 (hub), CO Thu 12/11 (hub), CO Fri 13/11 (hub) | running |
| E-10 | Corey | A first-person "my rule" answer to a big-vendor announcement beats a neutral summary | hook type: vendor news + own rule | CO Fri 13/11 09:20 (explore) | running |

Exploit/refine/explore: PE Thu exploit (C-02), PE Fri refine (C-04, new story), CO Thu refine (C-01 sourced-specifics angle in a hub), CO Fri explore (E-10). Step 3K: nothing created on Kristian's channel (no clean first-person material).

## Run of Fri 06/11/2026, second firing: Kristian posts Mon 09/11 and Thu 12/11
No new mature posts. First posts under the 06/11 first-person-opinion rule for his channel.
| id | channel | hypothesis | change | posts | status |
|---|---|---|---|---|---|
| E-11 | Kristian | A first-person "my read / what I'd check first" opinion on a public trending story, in a diagram infographic, holds his median (184) without any company material | topic source + format (explore) | KP Mon 09/11 hub (MCPhantom), KP Thu 12/11 flow (Conductor exit); keys end -kp | running |
Exploit/refine/explore: both explore (new rule, no clean past winner; C-04 MCP-diagram angle reused for Monday as refine of C-04). C-03 not replicable.

E-11 addendum (fri2 firing): third post KP Mon 16\/11 09:00 flow (hooks vs EDR, Anthropic 05\/11), explore.

## Run of Sun 08/11/2026: Saturday 14/11 (Presso, Corey)
Mature results: C-01 CONFIRMED (CO 05/11 20:30 flow, 13 impressions, lift 3.25 vs 1.3 bar; tiny n, treat as weak). New candidate C-05 (PE Mon 02/11 myths, 40, lift 2.2), replication = PE Tue 10/11 EDR myths (already scheduled, E-06). KP: nothing logged. E-01 to E-11 remain running; no experiment has 3 posts on both arms with a result worth closing.
| id | channel | hypothesis | change | posts | status |
|---|---|---|---|---|---|
| E-12 | Presso | A trending launch told as a hub diagram holds the 08:00 test slot | layout hub + time 08:00 | PE Sat 14/11 08:00 hub | running (refine of C-04) |
| E-13 | Corey | A first-person "what to agree before I work nights" checklist on a trending launch beats evergreen checklists (CO 06/11 steps got 0) | hook: first-person job-design + trending | CO Sat 14/11 08:00 steps | running (explore) |
Exploit/refine/explore: PE refine, CO explore. Both trending. KP: no post (3 already scheduled).

## Run of Wed 11/11/2026: Presso and Corey 16/11 to 18/11, Kristian 17/11 to 21/11
No new mature results read this run (measurement not refreshed, see learnings/2026-w46-wed.md). E-01 to E-13 stay running.
| id | channel | hypothesis | change | posts | status |
|---|---|---|---|---|---|
| E-14 | Presso, Corey | 20:30 beats the main slot (Decision row 38) | time | PE Wed 18/11 20:30 bars, CO Wed 18/11 20:30 flow | running (n now 2 more) |
| E-15 | Kristian | Publishing test: format x slot x type rotation (Notion plan 11/11/2026, Linear PRE-2026) | format, time, type | KP 17/11 to 21/11 (keys end -kp) | running until 10/01/2027 |
| E-16 | Corey | An AI co-founder confessing its own error rate ("I write wrong, fluently") draws comments (replicates E-05 hook type) | hook | CO Wed 18/11 | running (explore) |
Exploit/refine/explore: PE Mon refine (C-04 hub, trending), PE Tue explore (open-source tool type), PE Wed refine (C-02 hard numbers, evening); CO Mon refine (C-01 sourced specifics, hub to flow), CO Tue explore (how-to), CO Wed explore (E-16). Trending: PE Mon, PE Wed, CO Mon, CO Tue. Kristian: all explore under E-11/E-15.
