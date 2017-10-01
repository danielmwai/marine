var handleDatepicker = function() {
    $('#datepicker-voyage-start').datepicker({
        todayHighlight: true,
        autoclose: true
    });
    $('#datepicker-voyage-end').datepicker({
        todayHighlight: true,
        autoclose: true
    });
};


var handleWizardsValidation = function() {
	"use strict";
	$("#wizard").bwizard({ validating: function (e, ui) {
        $("#form_actions").hide();
         if (ui.index == 0) {
            // step-1 validation
            $("#form_actions").hide();
            if (false === $('form[name="form-wizard"]').parsley().validate('primary')) {
                return false;
            }
        } else if ((ui.index == 1) && (ui.nextIndex > ui.index)){
            // step-2 validation
            $("#form_actions").hide();
              if (false === $('form[name="form-wizard"]').parsley().validate('primary1')) {
                return false;
            }
        } else if ((ui.index == 2) && (ui.nextIndex > ui.index)) {
            // step-3 validation
            $("#form_actions").show();
            if (false === $('form[name="form-wizard"]').parsley().validate('primary2')) {
                return false;
            }
        } 

    }});
};

var FormWizardValidation = function () {
	"use strict";
    return {
        //main function
        init: function () {
            handleWizardsValidation();
            handleDatepicker();
        }
    };
}();