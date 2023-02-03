jQuery(function() {
    let tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    $('input[type="date"]').each(function(index, item) {

        if($(item).attr("value").match(/^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$/)){
            let [day, month, year] = $(item).attr("value").split('/');
            let result = [year, month, day].join('-');
            $(item).attr("value", result);
        }
    });

    const updateProfilePicturePreview = () => {
        if ($("#profile_picture-clear_id").is(":checked")){
            $("#profile_picture-preview").attr("src", "/static/global/img/person.svg");
        } else if ($("#id_profile_picture").prop('files').length > 0){
            $("#profile_picture-preview").attr("src", URL.createObjectURL($("#id_profile_picture").prop('files')[0]));
        } else {
            if ($("#profile_picture_column a").length > 0){
                $("#profile_picture-preview").attr("src", $("#profile_picture_column a")[0].href);
            } else {
                $("#profile_picture-preview").attr("src", "/static/global/img/person.svg");
            }
        }
    }

    $("#id_profile_picture").change(function(){
        updateProfilePicturePreview();
    });

    $("#profile_picture-clear_id").change(function(){
        updateProfilePicturePreview();
    })

    $('.auto-submit-filter-form').change(function(event) {
        let target = event.target;
        if (!(target.tagName == 'INPUT' && target.type == 'text')) {
            $( this ).submit();
        }
    });

    $('.auto-height-textarea').each(function(){
        $( this ).css("min-height", `${parseInt($( this ).css("height"))}px`)
    });

    $('.auto-height-textarea').on("input", function () {
        this.style.height = 0;
        this.style.height = (this.scrollHeight) + "px";
    });

    $('.modal-show').each(function(){
        let modal = new bootstrap.Modal(document.getElementById($( this ).attr('id')));
        modal.show();
    });

    $(".collapse-chevron-button").click(function(){
        if ($( this ).html().trim() == '<i class="bi bi-chevron-compact-down"></i>'){
            $( this ).html('<i class="bi bi-chevron-compact-up"></i>');
        } else {
            $( this ).html('<i class="bi bi-chevron-compact-down"></i>');
        }
    });

});