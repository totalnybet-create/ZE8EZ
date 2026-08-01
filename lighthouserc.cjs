module.exports = {
  ci: {
    collect: {
      startServerCommand: 'python3 -m http.server 8080',
      startServerReadyPattern: 'Serving HTTP',
      url: ['http://127.0.0.1:8080/'],
      numberOfRuns: 1,
      settings: {
        chromeFlags: '--headless --no-sandbox --disable-gpu'
      }
    },
    assert: {
      assertions: {
        'categories:performance': ['warn', { minScore: 0.8 }],
        'categories:accessibility': ['warn', { minScore: 0.9 }],
        'categories:best-practices': ['warn', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.9 }]
      }
    },
    upload: {
      target: 'filesystem',
      outputDir: './lighthouse-reports'
    }
  }
};
