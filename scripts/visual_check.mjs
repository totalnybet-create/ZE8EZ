import { chromium } from 'playwright';
import { mkdir } from 'node:fs/promises';

const baseUrl = process.env.ZE8ES_BASE_URL || 'http://127.0.0.1:4173';
const outputDir = process.env.ZE8ES_SCREENSHOT_DIR || 'visual-artifacts';
const viewports = [
  { name: 'desktop-1440', width: 1440, height: 1000 },
  { name: 'laptop-1024', width: 1024, height: 900 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'mobile-390', width: 390, height: 844 },
  { name: 'mobile-320', width: 320, height: 740 },
];

await mkdir(outputDir, { recursive: true });
const browser = await chromium.launch({ headless: true });
const failures = [];

for (const viewport of viewports) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    reducedMotion: 'reduce',
  });
  const page = await context.newPage();
  const browserErrors = [];

  page.on('console', (message) => {
    if (message.type() === 'error') browserErrors.push(`console: ${message.text()}`);
  });
  page.on('pageerror', (error) => browserErrors.push(`pageerror: ${error.message}`));
  page.on('requestfailed', (request) => {
    browserErrors.push(`requestfailed: ${request.url()} (${request.failure()?.errorText || 'unknown'})`);
  });

  try {
    const response = await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 30_000 });
    if (!response?.ok()) {
      failures.push(`${viewport.name}: strona zwróciła HTTP ${response?.status() ?? 'brak odpowiedzi'}`);
    }

    await page.locator('main').waitFor({ state: 'visible' });
    await page.locator('footer').scrollIntoViewIfNeeded();
    await page.waitForTimeout(250);

    const layout = await page.evaluate(() => ({
      viewportWidth: window.innerWidth,
      documentWidth: document.documentElement.scrollWidth,
      bodyWidth: document.body.scrollWidth,
      h1Count: document.querySelectorAll('h1').length,
      hasMain: Boolean(document.querySelector('main')),
      hasFooter: Boolean(document.querySelector('footer')),
    }));

    const overflow = Math.max(layout.documentWidth, layout.bodyWidth) - layout.viewportWidth;
    if (overflow > 1) failures.push(`${viewport.name}: poziome przewijanie ${overflow}px`);
    if (layout.h1Count !== 1) failures.push(`${viewport.name}: znaleziono ${layout.h1Count} elementów h1`);
    if (!layout.hasMain || !layout.hasFooter) failures.push(`${viewport.name}: brak main lub footer`);

    if (viewport.width <= 768) {
      const menuButton = page.locator('.menu-toggle');
      await menuButton.click();
      const expanded = await menuButton.getAttribute('aria-expanded');
      const mobileMenuVisible = await page.locator('#mobile-menu').isVisible();
      if (expanded !== 'true' || !mobileMenuVisible) failures.push(`${viewport.name}: menu mobilne nie otwiera się poprawnie`);
      await menuButton.click();
    }

    const firstFaq = page.locator('.faq-question').first();
    if (await firstFaq.count()) {
      await firstFaq.click();
      if ((await firstFaq.getAttribute('aria-expanded')) !== 'true') {
        failures.push(`${viewport.name}: FAQ nie aktualizuje aria-expanded`);
      }
    }

    await page.screenshot({
      path: `${outputDir}/${viewport.name}.png`,
      fullPage: true,
      animations: 'disabled',
    });

    if (browserErrors.length) failures.push(`${viewport.name}: ${browserErrors.join(' | ')}`);
  } catch (error) {
    failures.push(`${viewport.name}: ${error instanceof Error ? error.message : String(error)}`);
  } finally {
    await context.close();
  }
}

await browser.close();

if (failures.length) {
  console.error('Wykryto problemy w testach wizualnych:');
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log(`OK: zapisano ${viewports.length} zrzutów i nie wykryto błędów konsoli ani poziomego przewijania.`);
