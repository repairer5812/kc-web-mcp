const form = document.querySelector('#approval-form');
if (form) {
  const input = form.querySelector('#owner-token');
  const reveal = form.querySelector('.reveal');
  reveal.hidden = false;
  reveal.addEventListener('click', () => {
    const showing = input.type === 'password';
    input.type = showing ? 'text' : 'password';
    reveal.setAttribute('aria-pressed', String(showing));
    reveal.setAttribute('aria-label', showing ? '인증키 숨기기' : '인증키 표시');
  });
  form.addEventListener('submit', () => {
    const button = form.querySelector('[type=submit]');
    button.disabled = true;
    button.querySelector('span').textContent = '연결 승인 중…';
    form.setAttribute('aria-busy', 'true');
  });
  window.addEventListener('pageshow', () => {
    const button = form.querySelector('[type=submit]');
    button.disabled = false;
    button.querySelector('span').textContent = '연결 승인하기';
    form.removeAttribute('aria-busy');
  });
}
