document.addEventListener('DOMContentLoaded', function () {
    var modeSwitch = document.querySelector('.mode-switch');

    modeSwitch.addEventListener('click', function () {
        document.documentElement.classList.toggle('dark');
        modeSwitch.classList.toggle('active');
    });

    var listView = document.querySelector('.list-view');
    var gridView = document.querySelector('.grid-view');
    var songView = document.querySelector('.song-view');
    var cardView = document.querySelector('.card-view');
    var songSvg = document.querySelector('.song-svg');
    var cardSvg = document.querySelector('.card-svg');
    var songmView = document.querySelector('.songm-view');
    var cardmView = document.querySelector('.cardm-view');
    var songmSvg = document.querySelector('.songm-svg');
    var cardmSvg = document.querySelector('.cardm-svg');

    var walletView = document.querySelector('.wallet-view');
    var visaView = document.querySelector('.visa-view');
    var walletSvg = document.querySelector('.wallet-svg');
    var visaSvg = document.querySelector('.visa-svg');

    var reportView = document.querySelector('.report-view');
    var incomeView = document.querySelector('.income-view');
    var reportSvg = document.querySelector('.report-svg');
    var incomeSvg = document.querySelector('.income-svg');

    var editView = document.querySelector('.edit-view');
    var serviceView = document.querySelector('.service-view');
    var editSvg = document.querySelector('.edit-svg');
    var serviceSvg = document.querySelector('.service-svg');

    var playerView = document.querySelector('.player-view');
    var artistView = document.querySelector('.artist-view');
    var playerSvg = document.querySelector('.player-svg');
    var artistSvg = document.querySelector('.artist-svg');

    var projectsList = document.querySelector('.project-boxes');

    // listView.addEventListener('click', function () {
    //     gridView.classList.remove('active');
    //     listView.classList.add('active');
    //     projectsList.classList.remove('jsGridView');
    //     projectsList.classList.add('jsListView');
    // });
    //
    // gridView.addEventListener('click', function () {
    //     gridView.classList.add('active');
    //     listView.classList.remove('active');
    //     projectsList.classList.remove('jsListView');
    //     projectsList.classList.add('jsGridView');
    // });

    songView.addEventListener('click', function () {
        cardView.classList.remove('active');
        songView.classList.add('active');
        projectsList.classList.remove('jsSongView');
        projectsList.classList.add('jsCardView');
        songSvg.classList.add('fill-white')
        cardSvg.classList.remove('fill-white')
    });

    cardView.addEventListener('click', function () {
        cardView.classList.add('active');
        songView.classList.remove('active');
        songSvg.classList.remove('fill-white')
        cardSvg.classList.add('fill-white')
        projectsList.classList.remove('jsCardView');
        projectsList.classList.add('jsSongView');
    });


    songmView.addEventListener('click', function () {
        cardmView.classList.remove('active');
        songmView.classList.add('active');
        songmSvg.classList.add('fill-white')
        cardmSvg.classList.remove('fill-white')
        projectsList.classList.remove('jsSongMView');
        projectsList.classList.add('jsCardMView');
    });

    cardmView.addEventListener('click', function () {
        cardmView.classList.add('active');
        songmView.classList.remove('active');
        songmSvg.classList.remove('fill-white')
        cardmSvg.classList.add('fill-white')
        projectsList.classList.remove('jsCardMView');
        projectsList.classList.add('jsSongView');
    });

    walletView.addEventListener('click', function () {
        visaView.classList.remove('active');
        walletView.classList.add('active');
        walletSvg.classList.add('fill-white')
        visaSvg.classList.remove('fill-white')
        projectsList.classList.remove('jsVisaView');
        projectsList.classList.add('jsWalletView');
    });

    visaView.addEventListener('click', function () {
        visaView.classList.add('active');
        walletView.classList.remove('active');
        walletSvg.classList.remove('fill-white')
        visaSvg.classList.add('fill-white')
        projectsList.classList.remove('jsWalletView');
        projectsList.classList.add('jsVisaView');
    });

    reportView.addEventListener('click', function () {
        incomeView.classList.remove('active');
        reportView.classList.add('active');
        reportSvg.classList.add('fill-white')
        incomeSvg.classList.remove('fill-white')
        projectsList.classList.remove('jsIncomeView');
        projectsList.classList.add('jsWalletView');
    });

    incomeView.addEventListener('click', function () {
        incomeView.classList.add('active');
        reportView.classList.remove('active');
        reportSvg.classList.remove('fill-white')
        incomeSvg.classList.add('fill-white')
        projectsList.classList.remove('jsReportView');
        projectsList.classList.add('jsVisaView');
    });

    editView.addEventListener('click', function () {
        serviceView.classList.remove('active');
        editView.classList.add('active');
        editSvg.classList.add('fill-white')
        serviceSvg.classList.remove('fill-white')
        projectsList.classList.remove('jsEditView');
        projectsList.classList.add('jsServiceView');
    });

    serviceView.addEventListener('click', function () {
        serviceView.classList.add('active');
        editView.classList.remove('active');
        editSvg.classList.remove('fill-white')
        serviceSvg.classList.add('fill-white')
        projectsList.classList.remove('jsEditView');
        projectsList.classList.add('jsServiceView');
    });


    playerView.addEventListener('click', function () {
        artistView.classList.remove('active');
        playerView.classList.add('active');
        playerSvg.classList.add('fill-white')
        artistSvg.classList.remove('fill-white')
        projectsList.classList.remove('jsPlayerView');
        projectsList.classList.add('jsArtistView');
    });

    artistView.addEventListener('click', function () {
        artistView.classList.add('active');
        playerView.classList.remove('active');
        playerSvg.classList.remove('fill-white')
        artistSvg.classList.add('fill-white')
        // projectsList.classList.remove('jsPlayerView');
        // projectsList.classList.add('jsArtistView');
    });

    document.querySelector('.messages-btn').addEventListener('click', function () {
        document.querySelector('.messages-section').classList.add('show');
    });

    document.querySelector('.messages-close').addEventListener('click', function () {
        document.querySelector('.messages-section').classList.remove('show');
    });
});