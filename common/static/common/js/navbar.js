// common/static/common/js/navbar.js
document.addEventListener('DOMContentLoaded', () => {
    // notificationを閉じる処理
    const $deleteButtons = document.querySelectorAll('.notification > .delete');
    $deleteButtons.forEach($el => {
        $el.addEventListener('click', () => {
            $el.parentElement.classList.add('is-hidden');
        });
    });

    // navbar-burgerの処理
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if ($navbarBurgers.length > 0) {
        $navbarBurgers.forEach(el => {
            el.addEventListener('click', () => {
                const target = el.dataset.target;
                const $target = document.getElementById(target);
                el.classList.toggle('is-active');
                $target.classList.toggle('is-active');
            });
        });
    }
});
