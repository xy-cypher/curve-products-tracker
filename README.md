This repo focuses on methods to parse transactions with curve v2 contracts.

The idea is to make it generic for all curve pools. Docs will follow soon.

From bout3fiddy (anon) in [Curve telegram](https://t.me/curvefi/371256):
- I built this a while ago (not maintained) to track the underlying tokens in eth tricrypto2 lp positions
- You need an alchemy api key which you can get for free. It gives you archive node access for free
- I learnt something interesting. Initially when you seeded liquidity into the tricrypto2 pool, and when I tried to calc_withdraw_one_coin for your addr and for any of the tokens, it would often return a virtual machine error. I can send an example script to reproduce this if you wish.
- @michwill: For certain historic blocks, right?
- Yes
- @michwill: That's because that pool has a bug in how those view methods handle parameter ramps. It's not dangerous but annoying. Happens during changes of A and gamma
- Not all addresses were affected tho. Just for addresses with the most liquidity. So, yours.
