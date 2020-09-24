$(function() {
    var INDEX = 0;
    $("#chat-submit").click(function(e) {
        e.preventDefault();
        var msg = $("#chat-input").val();
        if (msg.trim() == '') {
            return false;
        }
        generate_message_self(msg, 'self');
        var buttons = [{
                name: 'Existing User',
                value: 'existing'
            },
            {
                name: 'New User',
                value: 'new'
            }
        ];

        var res;
        const proxyurl = "https://cors-anywhere.herokuapp.com/";
        const url = "https://7q539nw8rl.execute-api.ap-southeast-1.amazonaws.com/default/dynamodb_update?db_type=2&db_input=" + msg + "&session_key=SESSION_KEY";

        fetch(proxyurl + url) // https://cors-anywhere.herokuapp.com/https://example.com
            .then(response => response.text())
            .then(contents => generate_message_response(contents, 'user'))
            .catch(() => console.log("Can’t access " + url + " response. Blocked by browser?"))

    })

    function generate_message_self(msg) {
        INDEX++;
        var str = "";
        str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg self\">";
        str += "<p class = \"text_inlog_self\"> You asked: <\/p>";
        str += "          <div class=\"cm-msg-text\">";
        str += msg;
        str += "          <\/div>";
        str += "        <\/div>";
        $(".chat-logs").append(str);
        $("#cm-msg-" + INDEX).hide().fadeIn(300);
        $("#chat-input").val('');
        $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
    }

    function generate_message_response(msg) {
        // msg = {"Intent List": ["EmailAddress_Info", "EmailAddress_Information", "HousingCosts_Info", "Income_Info", "Name_Info", "weather_info", "What_Next"], "DynamoDB Response": {"ResponseMetadata": {"RequestId": "8A4ABLO7NQ8ICSBB0JEENEN51FVV4KQNSO5AEMVJF66Q9ASUAAJG", "HTTPStatusCode": 200, "HTTPHeaders": {"server": "Server", "date": "Wed, 23 Sep 2020 07:44:52 GMT", "content-type": "application/x-amz-json-1.0", "content-length": "2", "connection": "keep-alive", "x-amzn-requestid": "8A4ABLO7NQ8ICSBB0JEENEN51FVV4KQNSO5AEMVJF66Q9ASUAAJG", "x-amz-crc32": "2745614147"}, "RetryAttempts": 0}}, "Lex Response": {"ResponseMetadata": {"RequestId": "b47542b3-24a1-45a1-b1db-edddad413596", "HTTPStatusCode": 200, "HTTPHeaders": {"x-amzn-requestid": "b47542b3-24a1-45a1-b1db-edddad413596", "date": "Wed, 23 Sep 2020 07:44:52 GMT", "content-type": "application/json", "content-length": "345"}, "RetryAttempts": 0}, "slots": {}, "message": "Apologies, we can\u2019t answer this question.", "messageFormat": "PlainText", "dialogState": "Failed", "sessionId": "2020-09-23T07:44:14.851Z-PqyiSIKy"}};
        msg = JSON.parse(msg)['Lex Response'].message;
        // console.log(msg['Lex Response'].message);

        INDEX++;
        var str = "";
        str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg user\">";
        str += "<p class = \"text_inlog_response\"> Answered: <\/p>";
        str += "<div class=\"thumb_icons\" >"
        str += "<i class=\"fa fa-thumbs-up btn\"><\/i>"
        str += "<i class=\"fa fa-thumbs-down btn\"><\/i>"
        str += "          <\/div>";
        str += "          <div class=\"cm-msg-text\">";
        str += msg;
        str += "          <\/div>";
        str += "        <\/div>";
        $(".chat-logs").append(str);
        $("#cm-msg-" + INDEX).hide().fadeIn(300);
        $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
    }

    function generate_button_message(msg, buttons) {

        INDEX++;
        var btn_obj = buttons.map(function(button) {
            return "              <li class=\"button\"><a href=\"javascript:;\" class=\"btn btn-primary chat-btn\" chat-value=\"" + button.value + "\">" + button.name + "<\/a><\/li>";
        }).join('');
        var str = "";
        str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg user\">";
        str += "          <div class=\"cm-msg-text\">";
        str += msg;
        str += "          <\/div>";
        str += "          <div class=\"cm-msg-button\">";
        str += "            <ul>";
        str += btn_obj;
        str += "            <\/ul>";
        str += "          <\/div>";
        str += "        <\/div>";
        $(".chat-logs").append(str);
        $("#cm-msg-" + INDEX).hide().fadeIn(300);
        $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
        $("#chat-input").attr("disabled", true);
    }

    $(document).delegate(".chat-btn", "click", function() {
        var value = $(this).attr("chat-value");
        var name = $(this).html();
        $("#chat-input").attr("disabled", false);
        generate_message_self(name, 'self');
    })

    $("#chat-bottom").click(function() {
        $("#chat-bottom").slideToggle(200, "linear", function() {});
        setTimeout(function() {
            $(".chat-box").animate({
                height: 'toggle'
            });
        }, 400);

        document.getElementById("chat-input").focus();
    })


    $(".chat-box-toggle").click(function() {

        $(".chat-box").slideToggle(200, "linear", function() {});

        setTimeout(function() { $("#chat-bottom").show(); }, 400);

        // $("#chat-bottom").animate({
        //     height: 'toggle'
        // });
        // $(".chat-box").animate({
        //     height: 'toggle'
        // });
    })
})
