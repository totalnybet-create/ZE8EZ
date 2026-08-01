module.exports = {
  ci: {
    collect: {
      startServerCommand: 'python3 -m http.server 8080 --bind 127.0.0.1',
      startServerReadyPattern: 'Serving HTTP',
      url: ['http://127.0.0.1:8080/'],
      numberOfRuns: 3,
      settings: {
        chromeFlags: '--headless --no-sandbox --disable-gpu',
        emulatedFormFactor: 'mobile',
        throttlingMethod: 'simulate'
      }
    },
    assert: {
      preset: 'lighthouse:recommended',
      assertions: {
        'categories:performance': ['warn', { minScore: 0.85 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'categories:best-practices': ['error', { minScore: 0.95 }],
        'categories:seo': ['error', { minScore: 0.95 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 2200 }],
        'largest-contentful-paint': ['warn', { maxNumericValue: 2800 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['warn', { maxNumericValue: 300 }],
        'speed-index': ['warn', { maxNumericValue: 3400 }],
        'is-crawlable': 'off',
        'uses-responsive-images': 'off',
        'unsized-images': 'error'
      }
    },
    upload: {
      target: 'filesystem',
      outputDir: './lighthouse-reports'
    }
  }
};
