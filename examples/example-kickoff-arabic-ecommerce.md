# Example: kickoff of a bilingual (Arabic/English) e-commerce engagement

> FICTIONAL. "Example Appliances KSA" (أجهزة المثال) and every detail below are invented to show the interaction pattern.
> Never reuse these facts, numbers or URLs as data for a real project.

## What Claude does before asking anything

The user opens the session inside the store's Nuxt repository and writes in Saudi Arabic:

> أبغى أسوي SEO لموقعي، المبيعات من قوقل ضعيفة

Claude first inspects without asking:
- No `seo-engagement/` folder exists, so this is a new engagement.
- `nuxt.config.ts`: an i18n setup serving `/ar` and `/en`; SSR isn't disabled. Routes come from `pages/`. `useSeoMeta`/`useHead` are used on product pages only. `public/robots.txt` exists.
- Live site (3 requests): robots.txt allows everything; the sitemap at `/sitemap.xml` lists ~1,100 URLs (its generator isn't identified yet); product pages have Product JSON-LD; category pages have no canonical; filter URLs (`?brand=`, `?capacity=`) carry no canonical or `noindex`, so they're indexable.

Each of these is a question Claude no longer has to ask. All are recorded in `01-discovery.md` as **inferred (to confirm)**.

## Turn 1: orient, then one question with a recommended default

> تمام، طالعت بسرعة الكود والموقع قبل ما أسألك أي شي:
> - الموقع مبني على Nuxt بلغتين (عربي/إنجليزي)، والـ sitemap والـ robots شغالة.
> - صفحات المنتجات فيها Product schema، بس صفحات الأقسام (categories) ما فيها canonical، وروابط الفلاتر (الماركة والسعة) ما عليها canonical ولا noindex.
>
> قبل ما نبدأ أحتاج أعرف بأي mode نشتغل:
> 1. **Audit Only**: تقرير بالمشاكل مرتبة حسب الأولوية، بدون أي تعديل.
> 2. **Strategy & Planning**: التقرير + keyword research + خطة وroadmap.
> 3. **Execution** (أنصح فيه لأن الكود قدامنا): كل اللي فوق + تنفيذ التعديلات وحدة وحدة بعد موافقتك على كل تعديل.
>
> وش تفضّل نمشي عليه؟

## Turn 2 onward: one essential question at a time

After the user picks Execution, Claude asks only what changes the plan, in priority order:

1. "Which categories (split air conditioners, refrigerators, washing machines) bring the most profit, and which ones do you want to grow first?" This decides which templates are audited first.
2. "Do you have a showroom customers visit?" This decides whether the Local module applies.
3. "Is Search Console set up? If yes, could you export the Performance report for the last 3 months? I'll send the exact clicks." This feeds Stage 2. Claude can't be added as a Google user, so access comes through exports or a connector the user sets up.

Claude does **not** ask about the framework, the languages or the sitemap. It already knows them.

## G1 confirmation summary (in the user's language)

> هذا فهمي للمشروع، صحّحني لو فيه شي غلط:
>
> **النشاط:** Example Appliances KSA (أجهزة المثال)، أجهزة منزلية (مكيفات سبليت، ثلاجات، غسالات)، أونلاين فقط بدون معرض، توصيل لكل مناطق المملكة.
> **الهدف:** زيادة الطلبات من قوقل على أقسام المكيفات (كلامك: "أبغى الناس تلقانا لما يدوّرون على مكيف سبليت").
> **التحويل:** طلب أونلاين، والثاني طلب عرض سعر للشركات.
> **الموقع:** Nuxt، عربي وإنجليزي (/ar و /en)، تقريباً 1,100 رابط في الـ sitemap (بتاريخ اليوم).
> **الـ mode:** Execution، وكل تعديل بموافقتك.
> **الـ modules:** Technical ✓ (تركيز على الـ canonicals وروابط الفلاتر)، On-page ✓، Content ✓، Off-page ✓، Analytics ✓، Arabic ✓. Local ✗ لأنه ما فيه مكان يزوره العملاء.
> **للحين مو معروف (وما راح يوقف الـ audit):** المنافسين، والأرقام الحالية لأن Search Console ما انربط للحين.
>
> الخطوة الجاية: Stage 2، نشوف أي بيانات نقدر نوصل لها فعلاً. نكمل؟

## What this example demonstrates

- Inspect the code and the live site before asking anything.
- Ask one question per turn and recommend a default.
- Explain in Arabic and keep the SEO terms in English.
- Give a reason when a module is skipped (Local).
- Unknowns are named as unknowns, and no baseline numbers are guessed.
- Explicit G1 confirmation before the audit starts.
