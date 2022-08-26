var trigger = document.querySelector('#datePicker');
    var dateComponent = new DatePicker({
        el: document.querySelector('#calendar'),
        trigger: trigger,
        onchange: function (curr) {
            trigger.value = curr;
        }
    });

    trigger.onfocus = function () {
        dateComponent.show();
    };

    const fecha = document.getElementsByClassName('date');

    fecha[0].classList.toggle('fecha')