// Vercel Serverless Function: collects CSP violation reports.
//
// The site's Content-Security-Policy-Report-Only header (vercel.json) points
// both the legacy report-uri mechanism and the modern Reporting API
// report-to mechanism at this endpoint. Browsers pick whichever one they
// support, so this handler accepts both request shapes:
//
//   1. Legacy `report-uri` (Content-Type: application/csp-report)
//      Body: { "csp-report": { "document-uri": ..., "violated-directive": ..., ... } }
//
//   2. Modern Reporting API `report-to` (Content-Type: application/reports+json)
//      Body: [ { "type": "csp-violation", "url": ..., "body": { ... } }, ... ]
//
// No database, no external service — this just logs to Vercel's function
// logs so violations are visible while the policy stays in Report-Only mode.
// Always responds 204 No Content, the conventional response for report
// endpoints, even if the body is malformed or empty.

function readRawBody(req) {
  return new Promise((resolve) => {
    // If a body-parsing layer already gave us something, use it as-is.
    if (req.body !== undefined && req.body !== null) {
      resolve(req.body);
      return;
    }
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
    });
    req.on('end', () => resolve(data));
    req.on('error', () => resolve(''));
  });
}

function parseBody(raw) {
  if (raw === undefined || raw === null || raw === '') return null;
  if (typeof raw === 'object') return raw; // already parsed (e.g. by a framework)
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

function logLegacyReport(report) {
  console.warn('[csp-report] legacy csp-report violation', {
    documentUri: report['document-uri'],
    violatedDirective: report['violated-directive'],
    effectiveDirective: report['effective-directive'],
    blockedUri: report['blocked-uri'],
    disposition: report.disposition,
    originalPolicy: report['original-policy'],
    sourceFile: report['source-file'],
    lineNumber: report['line-number'],
    columnNumber: report['column-number'],
    statusCode: report['status-code'],
  });
}

function logReportingApiEntry(entry) {
  const body = entry && entry.body ? entry.body : {};
  console.warn('[csp-report] reports+json violation', {
    type: entry && entry.type,
    url: entry && entry.url,
    userAgent: entry && entry.user_agent,
    documentUri: body.documentURL || body.documentUri,
    violatedDirective: body.violatedDirective || body.effectiveDirective,
    effectiveDirective: body.effectiveDirective,
    blockedUri: body.blockedURL || body.blockedUri,
    disposition: body.disposition,
    sourceFile: body.sourceFile,
    lineNumber: body.lineNumber,
    columnNumber: body.columnNumber,
    statusCode: body.statusCode,
  });
}

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') {
    res.statusCode = 204;
    res.end();
    return;
  }

  try {
    const raw = await readRawBody(req);
    const parsed = parseBody(raw);

    if (Array.isArray(parsed)) {
      // Modern Reporting API: an array of report objects.
      for (const entry of parsed) {
        if (entry && entry.type === 'csp-violation') {
          logReportingApiEntry(entry);
        } else if (entry) {
          console.warn('[csp-report] unrecognized report entry', entry);
        }
      }
    } else if (parsed && typeof parsed === 'object' && parsed['csp-report']) {
      // Legacy report-uri format.
      logLegacyReport(parsed['csp-report']);
    } else if (parsed) {
      console.warn('[csp-report] unrecognized report body', parsed);
    } else {
      console.warn('[csp-report] empty or unparsable report body received');
    }
  } catch (err) {
    // Never let a malformed report crash the endpoint.
    console.warn('[csp-report] failed to process report', err && err.message);
  }

  res.statusCode = 204;
  res.end();
};
