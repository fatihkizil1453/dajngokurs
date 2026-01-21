// estimator.js — lightweight UI interactivity and AJAX submission
// - intercepts form submit, sends data via fetch to backend JSON endpoint
// - animates the result box when response arrives

(function () {
  'use strict';

  function getCookie(name) {
    // small helper for CSRF token retrieval
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  const form = document.getElementById('estimate-form');
  if (!form) return;

  const resultBox = document.getElementById('estimate-result');
  const submitBtn = form.querySelector('button[type="submit"]');

  function formatTRY(amount) {
    try {
      return Number(amount).toLocaleString('tr-TR', { style: 'currency', currency: 'TRY', minimumFractionDigits: 2 });
    } catch (e) {
      return '₺ ' + Number(amount).toFixed(2);
    }
  }


  function showResult(payload) {
    if (!resultBox) return;
    let html = '';
    if (payload.base) {
      html += `<div class="small text-muted">Taban fiyat</div><div class="fw-semibold">${formatTRY(payload.base)}</div>`;
    }
    if (payload.enhanced) {
      html += `<div class="small text-muted mt-2">Konum / ulaşım dahil</div><div class="fw-semibold">${formatTRY(payload.enhanced)}</div>`;
    }
    html += `<div class="fs-3 fw-bold text-primary mt-3">${formatTRY(payload.result)}</div>`;
    resultBox.innerHTML = html;
    // animate
    resultBox.classList.remove('result-hidden');
    // trigger layout then add visible
    requestAnimationFrame(() => {
      resultBox.classList.add('result-visible');
      // small celebratory burst animation
      if (typeof window.__estimatorBurst === 'function') {
        window.__estimatorBurst(resultBox);
      }
    });
  }


  // Public burst helper so server-rendered inline scripts can reuse the animation
  window.__estimatorBurst = function (el) {
    if (!el) return;
    // make sure the container is positioned so absolutely positioned dots are visible
    el.style.position = 'relative';
    const colors = ['#00c6ff', '#0072ff', '#44d9b6', '#66a3ff', '#b5f3ff'];
    const dots = 10;
    for (let i = 0; i < dots; i++) {
      const dot = document.createElement('span');
      dot.className = 'burst-dot';
      // random color and placement near center
      dot.style.left = (50 + (Math.random() - 0.5) * 60) + '%';
      dot.style.top = (40 + (Math.random() - 0.5) * 40) + '%';
      dot.style.background = colors[Math.floor(Math.random() * colors.length)];
      // random size
      const size = 6 + Math.floor(Math.random() * 8);
      dot.style.width = size + 'px';
      dot.style.height = size + 'px';
      el.appendChild(dot);
      // remove after animation completes
      setTimeout(() => { dot.remove(); }, 900 + Math.random() * 400);
    }
  };

  form.addEventListener('submit', function (ev) {
    // progressive enhancement: allow normal post if JS disabled
    ev.preventDefault();

    // disable button while submitting
    submitBtn.disabled = true;
    submitBtn.classList.add('opacity-75');

    const formData = new FormData(form);
    const body = new URLSearchParams();
    for (const pair of formData.entries()) body.append(pair[0], pair[1]);

    const headers = {
      'X-Requested-With': 'XMLHttpRequest',
      'X-CSRFToken': getCookie('csrftoken') || ''
    };

    fetch('.', { method: 'POST', body: body, headers: headers })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          // server returns numeric fields: result, base, enhanced
          // pass through to showResult so formatting happens client-side
          showResult({ result: Number(data.result), base: Number(data.base), enhanced: Number(data.enhanced) });
        } else if (data.errors) {
          // display first non-field error or field errors
          const err = data.errors.__all__ || data.errors;
          // simple alert for now
          alert('Form error: ' + JSON.stringify(err));
        }
      })
      .catch(err => {
        console.error('Error fetching estimate', err);
        alert('Unexpected error — try again.');
      })
      .finally(() => {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75');
      });
  });

  // sync location slider to readout
  const locInput = form.querySelector('[name="location_rating"]');
  const locReadout = document.getElementById('loc-readout');
  if (locInput && locReadout) {
    const update = () => { locReadout.textContent = locInput.value; };
    update();
    locInput.addEventListener('input', update);
  }
})();
