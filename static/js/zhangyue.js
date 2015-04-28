$(document).ready(function(){
  $("#setting_btn1").click(function(){
        if($("#name").val()=="" || $("#weizhi").val()=="" || $("#tel").val()=="" || $("#kefu").val()=="" || $("#jigui").val()==""){
		//$("#warning-block").show();
		alert("请不要输入空元素");
        }else{
                $.post("/shezhi/",
                {
                        name:	$("#name").val(),
                        weizhi:	$("#weizhi").val(),
                        tel:	$("#tel").val(),
                        kefu:	$("#kefu").val(),
                        jigui:	$("#jigui").val(),
                },
                        function(status){
				alert("保存成功");
                });
				location.href='/idc_manager/';
        };
  });
//********************

  $("#setting_btn2").click(function(){
        if($("#user").val()=="" || $("#passwd").val()=="" || $("#passwd2").val()=="" || $("#email").val()=="" || $("#tel").val()==""){
                alert("请不要输入空元素");
	}else  if ($("#passwd").val()!=$("#passwd2").val())
  		{
		alert("两次输入密码不一致");
  		}

	else{
                $.post("/useradd/",
                {
                        user:   $("#user").val(),
                        passwd: $("#passwd").val(),
                        email:  $("#email").val(),
                        tel:  	$("#tel").val(),
			sele:	$('#sele option:selected').text(),
			role:   $("#sele option:selected").val(),
			priv:   $('input:radio[name="optionsRadiosinline"]:checked').val(),
                },
                        function(status){
                                alert("保存成功");
                });
				location.href='/user/';
        };
  });

////////////////////////////////////////////////////////////////
    $("#del_user").click(function () {
        var $radio= $("#table input:radio:checked");
	var $row=$radio.val();
	var $deparment=$("#table tr:eq("+$row+") td:nth-child(5)").html();
	var $account=$("#table tr:eq("+$row+") td:nth-child(2)").html();
        //alert($row);
	//alert($deparment);
	del ($account,$deparment);
   	});
	function del($account,$deparment){
  		var msg = "确定要删除吗?"; 
  		if (confirm(msg)==true){ 
		     $.post("/userdel/",
                     {
                        account:   $account,
                        deparment: $deparment,
                     },
                        function(status){
                                alert("删除成功");
                     });
                        location.href='/user/';
  		}else{ 
			return false;
  	             }		 

   	}

});


