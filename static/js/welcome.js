// ============================
// >> WELCOME PAGE
// ============================


// var guildStatusRank = {
//     'currentMember': 1,
//     'exMember': 1,
//     'other': 1,
//     '': 1,
// }

// Helper function to insert users in html table
function insertUserToTable(index, table, user, excess, prioLimit) {
    $("#registeredUsers").find('tbody')
    .append($('<tr>')
        .append($('<td>')
            .text(function() {
                if (index > MAX_USERS) return index + ' (jono)';
                return index;
            })
        )
        .append($('<td>')
            .text(user.name.substring(0, 36))
            .css('word-break', 'break-word')
        )
        .append($('<td>')
            .text(user.table.substring(0, 36))
            .css('word-break', 'break-all')
        )
        .css('borderBottom', function() {
            if (index === MAX_USERS) return '2px dotted #0DFF92';
            return '1px solid #1f0044';
        })
    );
}

// On page load get users and insert them to table
$(function() {
    var table = document.getElementById('registeredUsers');
    $.ajax({
        url: API_BASE_URL + '/users',
        type: "GET",
        success: function(response) {
            var rawUsersData = JSON.parse(response);
            // var preUsers = rawUsersData.filter(
            //     function(u) {
            //         return !!u.preRegistration;
            //     }
            // );
            // var preUsers = preUsers.sort(
            //     function(a, b) {
            //         return a.timestamp - b.timestamp;
            //     }
            // );

            // var regularUsers = rawUsersData.filter(
            //     function(u) {
            //         return !u.preRegistration;
            //     }
            // );
            // var regularUsers = regularUsers.sort(
            //     function(a, b) {
            //         var aRank = guildStatusRank[a.guildStatus];
            //         var bRank = guildStatusRank[b.guildStatus];
            //         if (aRank !== bRank) {
            //             return aRank - bRank;
            //         } else {
            //             return a.timestamp - b.timestamp;
            //         }
            //     }
            // );
            // var usersData = preUsers.concat(regularUsers);

            // var priorityUsers = usersData.filter(
            //     function(u) {
            //         return !!u.preRegistration || u.guildStatus === 'currentMember';
            //     }
            // );
            // var count = priorityUsers.length;
            // console.log('pre-registration + current members : ' + count);
            var usersData = rawUsersData.sort(
                function(a, b) {
                    return a.timestamp - b.timestamp;
                }
            );
            // if (priorityUsers.length < 456 && (new Date()).getTime() >= 1485770400000) {
            var now = (new Date()).getTime();
            // if (now > 1518429600000 && now < 1520027700000) {
            $('#registrationButtonContainer').removeClass('hidden');
            // }
            // }
            // var excess = false;
            // var prioLimit = false;
            for (var i = 0; i < usersData.length; i++) {
                //     if (i >= 455) {
                //         excess = true;
                //     }
                //     if (i == count - 1) {
                //         prioLimit = true;
                //     }
                insertUserToTable(i + 1, table, usersData[i]);
                // insertUserToTable(i + 1, table, usersData[i], excess, prioLimit);
                // prioLimit = false;
            }
       
        },
        error: function(response) {
            console.error('ERROR', response);
        },
    });
});
