# همپوشانی quorum در Flexible Paxos

آیا همه‌ی quorumهای Paxos باید اکثریت باشند؟ برای ۳ تا ۷ عضو acceptor، این آزمایش هر quorum انتخابی (فاز ۱) به اندازه‌ی Q₁ و هر quorum replicationی (فاز ۲) به اندازه‌ی Q₂ را برمی‌شمارد. می‌سنجد که هر جفتی همیشه همپوشانی دارد یا نه، و اگر جفتی جدا باشد چاپش می‌کند. نشان می‌دهد هر فاز چند شکست را تاب می‌آورد، و حساب PBFT را برای n = 3f + 1 می‌کند.

*تصویری از «Flexible Paxos» کتاب Database Internals، صص. ۲۹۶–۲۹۷ (تنها Q₁ + Q₂ > N لازم است) و «الگوریتم PBFT»، ص. ۳۰۶ (رابطه‌ی n = 3f + 1 و quorumهای 2f و 2f + 1). آن سنجش جست‌وجوی فراگیر مال خود vault است.*

## اجرا

نسخه‌ی Python ۳.۱۰ یا بالاتر، تنها کتابخانه‌ی استاندارد، قطعی با seed:

```sh
python3 flexible_paxos.py
```

## خروجی چشم‌داشته

```text
Safe (Q1, Q2) pairs: every election quorum meets every replication quorum

N=3: safe exactly when Q1 + Q2 > 3; minimal pairs (3,1) (2,2) (1,3)
N=4: safe exactly when Q1 + Q2 > 4; minimal pairs (4,1) (3,2) (2,3) (1,4)
N=5: safe exactly when Q1 + Q2 > 5; minimal pairs (5,1) (4,2) (3,3) (2,4) (1,5)
N=6: safe exactly when Q1 + Q2 > 6; minimal pairs (6,1) (5,2) (4,3) (3,4) (2,5) (1,6)
N=7: safe exactly when Q1 + Q2 > 7; minimal pairs (7,1) (6,2) (5,3) (4,4) (3,5) (2,6) (1,7)

N=5 configurations
 Q1  Q2  safe  election survives  replication survives
  3   3   yes            2 failed               2 failed
  4   2   yes            1 failed               3 failed
  5   1   yes            0 failed               4 failed
  3   2    no            2 failed               3 failed   e.g. {0, 1, 2} and {3, 4} are disjoint

PBFT: n = 3f + 1, commit quorum 2f + 1
 f   n  prepare 2f  commit 2f+1  min overlap  honest in overlap
 1   4           2            3            2                  1
 2   7           4            5            3                  1
 3  10           6            7            4                  1
```

## به چه چیزی نگاه کنید

- آن جست‌وجوی فراگیر با قاعده‌ی کتاب می‌خواند: چیدمانی ایمن است دقیقاً وقتی Q₁ + Q₂ > N.
- با پنج acceptor، مقدار Q₁ = 4 و Q₂ = 2 ایمن است. replication بعد سه شکست را تاب می‌آورد، ولی انتخابی تازه چهار acceptor زنده می‌خواهد: همان بده‌بستان availability در برابر latency در ص. ۲۹۷.
- با Q₁ = 3 و Q₂ = 2 جفتی جدا هست، پس leaderی تازه می‌تواند مقداری را که آن قدیمی replication کرده بود از دست بدهد.
- در PBFT، هر دو quorum تأییدی به اندازه‌ی 2f + 1 دست‌کم در f + 1 نسخه همپوشانی دارند، پس دست‌کم یک نسخه‌ی درست‌کار در هر دو هست.

## مرتبط

- یادداشت فصل: [فصل ۱۴: consensus](../../chapters/14-consensus.md) — «Flexible Paxos»، صص. ۲۹۶–۲۹۷؛ «الگوریتم PBFT»، ص. ۳۰۶
