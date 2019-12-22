// Empty JS for your own code to be here
 function upload_cover() {
            if (document.getElementById('cover').files == 0)
                return;
            let cover = new FormData();
            let fileObj = document.getElementById('cover').files[0];

            cover.append('cover', fileObj)
            $.ajax({
                type: 'post',
                url: '/upload_cover',
                data: cover,
                async: false,
                processData: false,
                contentType: false,
                success: function (data, status) {
                    if (data['status'] == 'error') {
                        alert(data['msg']);
                    } else {
                        document.getElementById('icon').src = data['url'];
                    }
                },
            });
        }