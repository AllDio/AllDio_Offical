const rawProductData = [
    [
        {
            productTitle: "CVS Health Non-Drowsy Allergy Relief Tablets, 70 CT",
            price: "24.99"
        },
    ],
    [
        {
            productTitle: "Pocket Mouse Wireless Mouse You Hold Like A Pen",
            price: "19.99"
        },
    ],
];

let couponID = 0;

function randomMinMax(min, max) {
    return Math.floor(Math.random() * max) + min;
}

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

function populate() {
    while (true) {
        let coupons = document.getElementById("coupons");
        let windowRelativeBottom = document.documentElement.getBoundingClientRect()
            .bottom;
        if (windowRelativeBottom > document.documentElement.clientHeight + 100) break;
        getCoupon();
    }
}

// THINGS NEEDED FOR COUPON
// Current Date to set EXPIRATION DATE
// Product Name
// Product Price -- used to determine coupon value
// 20 Digit Barcode
// 5 Digit Coupon #
// Price Off / Discount
// Discount Description

function newCoupon(discount, description, value) {
    //couponID & barcode will be done here automatically
    this.discount = discount;
    this.description = description;
    this.value = value;
    this.barcode = randomBarcode();
    this.couponCode = randomMinMax(10000, 90000);
}

function formatCoupon(coupon) {
    let coupons = document.getElementById("coupons");
    coupons.insertAdjacentHTML(
        "beforeend",
        `
        <div class="couponContainer">
          <h1 class="logo">CVS/pharmacy</h1>
          <div class="discount">${coupon.discount}</div>
          <div class="discountDetails">${coupon.discount} ${
            coupon.description
        }</div>
          <div class="expiration">
            <div class="item bold">
              Expires 12/12/2018
            </div>
            <div class="item">
             ${coupon.value}
            </div>
          </div>
          <div class="barcode">
            HelloCVSMate1
          </div>
          <div class="barcodeID center">
            ${coupon.barcode}
          </div>
          <div class="legal center">
            ExtraCare card required. Excludes lottery, money orders, postage stamps, milk, prescriptions, pre-paid cards, gift cards, pseudoephedrine products, other fees, deposits, taxes, alcohol and local exclusions. No cash back. Tax charged on pre-coupon price
            where required. Limit of one purchase-based coupon, i.e., $4 off $20 purchase, per transaction. Not valid in specialty centers within CVS.
          </div>
          <div class="couponBottom">
            <p>ExtraCare Card #: *7140 00130030598777</p>
            <p>CPN#: ${coupon.couponCode}</p>
          </div>
        </div>
      `
    );
}

// THINGS NEEDED FOR COUPON
// Current Date to set EXPIRATION DATE
// Dollar Rewards $1-10
// 18 Digit Barcode
// 5 Digit Coupon #

randomBarcode = () => {
    //make 18 digit barcode
    // 4 4 4 4 2
    return `${randomMinMax(1000, 9000)}
  ${randomMinMax(1000, 9000)}
  ${randomMinMax(1000, 9000)}
  ${randomMinMax(1000, 9000)}
  ${randomMinMax(10, 90)}`;
};

getProduct = () => {
    let products = rawProductData.flat(2); // not recursive -- fixed flatten based on the data below 🤷
    let productId = getRandomInt(products.length);
    return products[productId];
};

percentCoupon = () => {
    const percentOptions = [5, 10, 15, 20, 25, 50]; //popular discount options
    let randomPercent = percentOptions[getRandomInt(percentOptions.length)];
    randomPercent = `${randomPercent}% off`;
    let product = getProduct();
    let newCoup = new newCoupon(
        randomPercent,
        product.productTitle,
        "Up to $99 value"
    );
    return formatCoupon(newCoup);
};

fixedCoupon = () => {
    //max discount is 50% off
    // productPrice x .5 = discountTakenOff
    // i.e. $10 product get random number between 0.01  and 5 ...
    // so a user will get $5 off an item which would be 50% off

    let product = getProduct();
    let couponValue = Math.round(parseFloat(product.price) * 0.5);
    let discountPrice = `$${couponValue}.00 off`;
    couponValue = `Up to $${couponValue} value`;
    let newCoup = new newCoupon(discountPrice, product.productTitle, couponValue);
    return formatCoupon(newCoup);
};

buckCoupon = () => {
    console.log("BUCK", couponID);
};

getCoupon = () => {
    couponID++;
    if (couponID % 13 == 0) {
        // every 13th coupon load a BUCKs
        buckCoupon();
    } else {
        const coupons = ["percent", "fixed"];
        let randomCoupon = getRandomInt(coupons.length);
        switch (randomCoupon) {
            case 0:
                fixedCoupon();
                break;
            default:
                percentCoupon();
        }
    }
};

window.addEventListener("scroll", populate);

populate(); // init document
