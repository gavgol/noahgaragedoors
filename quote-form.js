(function () {
    'use strict';

    var endpoint = 'https://noah-fsm.vercel.app/api/website-leads';
    var websiteKey = 'wlead_LDLD800Fz7MdmcDaQ4Bdi00jHp05Q7FH';
    var form = document.getElementById('quoteForm');
    if (!form) return;

    var submitButton = document.getElementById('quoteSubmit');
    var submitText = document.getElementById('quoteSubmitText');
    var errorBox = document.getElementById('formError');
    var successBox = document.getElementById('formSuccess');
    var sourceInput = document.getElementById('leadSource');
    var startedInput = document.getElementById('formStartedAt');
    var params = new URLSearchParams(window.location.search);

    startedInput.value = String(Date.now());
    sourceInput.value = leadSource(params);

    function leadSource(searchParams) {
        var source = searchParams.get('utm_source');
        var campaign = searchParams.get('utm_campaign');
        if (source) return source + (campaign ? ' / ' + campaign : '');
        if (!document.referrer) return 'Direct';
        if (/facebook|fb\.|instagram/i.test(document.referrer)) return 'Facebook/Instagram';
        if (/google/i.test(document.referrer)) return 'Google';
        if (/bing|yahoo|duckduckgo/i.test(document.referrer)) return 'Other search';
        return document.referrer;
    }

    function value(name) {
        var field = form.elements.namedItem(name);
        return field && typeof field.value === 'string' ? field.value.trim() : '';
    }

    function setSending(sending) {
        submitButton.disabled = sending;
        submitText.textContent = sending ? 'Sending...' : 'Request Free Quote \u2192';
    }

    function showError(message) {
        errorBox.textContent = message;
        errorBox.classList.remove('hidden');
        errorBox.focus();
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        errorBox.classList.add('hidden');

        if (!form.reportValidity()) return;

        setSending(true);
        var payload = {
            name: value('name'),
            phone: value('phone'),
            service: value('service'),
            message: value('message'),
            sms_consent: (function () {
                var c = form.elements.namedItem('sms_consent');
                return !!(c && c.checked);
            })(),
            sms_consent_service: (function () {
                var c = form.elements.namedItem('sms_consent_service');
                return !!(c && c.checked);
            })(),
            source: value('lead_source'),
            website: value('website'),
            form_started_at: Number(value('form_started_at')),
            page_url: window.location.href,
            referrer: document.referrer,
            utm_source: params.get('utm_source') || '',
            utm_medium: params.get('utm_medium') || '',
            utm_campaign: params.get('utm_campaign') || '',
            utm_content: params.get('utm_content') || '',
            utm_term: params.get('utm_term') || '',
            gclid: params.get('gclid') || '',
            fbclid: params.get('fbclid') || '',
            msclkid: params.get('msclkid') || ''
        };

        try {
            var response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Website-Key': websiteKey
                },
                body: JSON.stringify(payload)
            });
            var result = await response.json().catch(function () { return {}; });
            if (!response.ok || !result.ok) {
                throw new Error(result.error || 'We could not send your request. Please call (619) 572-4266.');
            }

            form.classList.add('hidden');
            successBox.classList.remove('hidden');
            successBox.scrollIntoView({ behavior: 'smooth', block: 'center' });

            if (typeof window.gtag === 'function') {
                window.gtag('event', 'generate_lead', {
                    event_category: 'lead',
                    event_label: 'quote_form',
                    source: 'website_quote_form'
                });
            }
            if (typeof window.fbq === 'function') {
                window.fbq('track', 'Lead', { content_name: 'quote_form' });
            }
        } catch (error) {
            showError(error instanceof Error ? error.message : 'We could not send your request. Please call (619) 572-4266.');
            setSending(false);
        }
    });
})();
