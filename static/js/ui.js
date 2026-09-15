// Progressive enhancement: the original POST forms also work without JavaScript.
const promptInput = document.querySelector('#entrada');
document.querySelectorAll('[data-prompt]').forEach(button => {
    button.addEventListener('click', () => {
        promptInput.value = button.dataset.prompt;
        promptInput.focus();
    });
});

const tracks = [...document.querySelectorAll('input[name="seleccionadas"]')];
const selectAll = document.querySelector('#select-all');
const count = document.querySelector('#selection-count');
function updateSelection() {
    const selected = tracks.filter(track => track.checked).length;
    if (count) count.textContent = `${selected} seleccionada${selected === 1 ? '' : 's'}`;
    if (selectAll) {
        selectAll.checked = selected === tracks.length;
        selectAll.indeterminate = selected > 0 && selected < tracks.length;
    }
}
selectAll?.addEventListener('change', () => {
    tracks.forEach(track => { track.checked = selectAll.checked; });
    updateSelection();
});
tracks.forEach(track => track.addEventListener('change', updateSelection));
updateSelection();

document.querySelectorAll('audio').forEach(player => {
    player.addEventListener('play', () => {
        document.querySelectorAll('audio').forEach(other => { if (other !== player) other.pause(); });
    });
});

document.querySelectorAll('form[data-loading]').forEach(form => {
    form.addEventListener('submit', event => {
        if (form.dataset.busy === 'true') { event.preventDefault(); return; }
        form.dataset.busy = 'true';
        form.setAttribute('aria-busy', 'true');
        // Keep the submitter enabled so its name/value (sorprendeme) is posted.
        form.querySelectorAll('button[type="submit"]').forEach(button => button.setAttribute('aria-disabled', 'true'));
        const status = form.querySelector('.loading-status') || form.parentElement.querySelector('.loading-status');
        if (status) status.textContent = form.dataset.loading;
    });
});

// Restore the controls when returning with the browser's Back button.
window.addEventListener('pageshow', () => {
    document.querySelectorAll('form[data-loading]').forEach(form => {
        delete form.dataset.busy;
        form.removeAttribute('aria-busy');
        form.querySelectorAll('[aria-disabled]').forEach(button => button.removeAttribute('aria-disabled'));
    });
    document.querySelectorAll('.loading-status').forEach(status => { status.textContent = ''; });
    updateSelection();
});
