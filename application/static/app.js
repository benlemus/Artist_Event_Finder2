document.addEventListener("DOMContentLoaded", async () => {
  if (document.querySelector("#featured-events")) {
    const topArtistList = document.getElementById("top-artist-list");
    const featuredEventsContainer = document.getElementById("featured-events");

    try {
      const res = await axios.get("/top-artists-events");
      const data = await res.data;
      const wishlist = await axios.get("/get-wishlist");

      topArtistList.innerHTML = "";

      data.forEach((eventGroup, index) => {
        const featuredEvents = document.createElement("div");
        featuredEvents.className = "row row-cols-xs-1 row-cols-sm-2";

        const carouselItem = document.createElement("div");
        if (index == 0) {
          carouselItem.className = "carousel-item active";
        } else {
          carouselItem.className = "carousel-item";
        }
        const cardGroup = document.createElement("div");
        cardGroup.className = "card-group";

        if (index == 0 || index == 1) {
          eventGroup.forEach((event, index) => {
            const newFeatured = document.createElement("div");
            newFeatured.className = "col";

            const featureCard = document.createElement("div");
            featureCard.className = "card m-3";
            featureCard.style.maxWidth = "800px";
            featureCard.style.minHeight = "300px";
            featureCard.style.maxHeight = "300px";

            const fRow = document.createElement("div");
            fRow.className = "row g-0";
            fRow.style.minHeight = "300px";

            const fImgCol = document.createElement("div");
            fImgCol.className = "col-md-4";

            const fImg = document.createElement("img");
            fImg.className = "img-fluid rounded-start grid-card-img";
            fImg.src = event.image;

            const fBodyCol = document.createElement("div");
            fBodyCol.className = "col-md-8";

            const fBody = document.createElement("div");
            fBody.className = "card-body";

            const fTitle = document.createElement("h3");
            fTitle.className = "card-title";
            fTitle.textContent = event.name;

            const fCity = document.createElement("p");
            fCity.className = "card-text";
            fCity.textContent = event.location;

            const fDate = document.createElement("p");
            fDate.className = "card-text";
            fDate.textContent = event.date;

            const fArtist = document.createElement("h5");
            fArtist.className = "card-title";
            fArtist.textContent = event.artist;

            const fTicketBtn = document.createElement("a");
            fTicketBtn.className = "btn btn-primary";
            fTicketBtn.textContent = "Get Tickets";
            fTicketBtn.href = event.url;

            const fWishBtn = document.createElement("a");
            if (wishlist.data.includes(event.event_id)) {
              fWishBtn.className = "btn btn-danger ms-3 wishlistBtn";
              fWishBtn.textContent = "Remove from Wishlist";
              fWishBtn.dataset.eventid = event.event_id;
            } else {
              fWishBtn.className = "btn btn-success ms-3 wishlistBtn";
              fWishBtn.textContent = "Add to Wishlist";
              fWishBtn.dataset.eventid = event.event_id;
            }

            fBody.append(fTitle, fCity, fDate, fArtist, fTicketBtn, fWishBtn);
            fBody.style.fontSize = "20px";
            fBodyCol.append(fBody);
            fImgCol.append(fImg);

            fRow.append(fImgCol, fBodyCol);
            featureCard.append(fRow);
            newFeatured.append(featureCard);
            featuredEvents.append(newFeatured);
            featuredEventsContainer.append(featuredEvents);
          });
        }

        eventGroup.forEach((event) => {
          const card = document.createElement("div");
          card.className = "card";

          const cardImg = document.createElement("img");
          cardImg.src = event.image;
          cardImg.className = "card-img-top";
          cardImg.style = "max-height: 230px";

          const cardBody = document.createElement("div");
          cardBody.className = "card-body";

          const cardTitle = document.createElement("h5");
          cardTitle.className = "card-title";
          cardTitle.textContent = event.name;

          const cardCity = document.createElement("p");
          cardCity.className = "card-text";
          cardCity.textContent = event.location;

          const cardDate = document.createElement("p");
          cardDate.className = "card-text";
          cardDate.textContent = event.date;

          const cardArtist = document.createElement("h5");
          cardArtist.className = "card-title";
          cardArtist.textContent = event.artist;

          const cardTicketBtn = document.createElement("a");
          cardTicketBtn.className = "btn btn-primary";
          cardTicketBtn.textContent = "Get Tickets";
          cardTicketBtn.href = event.url;

          const cardWishBtn = document.createElement("a");
          if (wishlist.data.includes(event.event_id)) {
            cardWishBtn.className = "btn btn-danger ms-3 wishlistBtn";
            cardWishBtn.textContent = "Remove from Wishlist";
            cardWishBtn.dataset.eventid = event.event_id;
          } else {
            cardWishBtn.className = "btn btn-success ms-3 wishlistBtn";
            cardWishBtn.textContent = "Add to Wishlist";
            cardWishBtn.dataset.eventid = event.event_id;
          }

          cardBody.append(
            cardTitle,
            cardCity,
            cardDate,
            cardArtist,
            cardTicketBtn,
            cardWishBtn
          );

          card.append(cardImg, cardBody);
          cardGroup.append(card);
        });
        carouselItem.append(cardGroup);
        topArtistList.append(carouselItem);
      });
    } catch (error) {
      console.log("Error getting top artist events:", error);
      topArtistList.innerHTML = "<h3> Could Not Get Events... </h3>";
    }
  }
});

document.addEventListener("click", async (event) => {
  if (event.target.classList.contains("wishlistBtn")) {
    const button = event.target;
    const eventId = button.getAttribute("data-eventid");
    button.disabled = true;

    try {
      let response;
      if (button.textContent.trim() === "Add to Wishlist") {
        response = await axios.post(`/add-to-wishlist/${eventId}`);
        if (response.status === 200) {
          button.classList.replace("btn-success", "btn-danger");
          button.textContent = "Remove from Wishlist";
        }
      } else if (button.textContent.trim() === "Remove from Wishlist") {
        response = await axios.post(`/remove-wishlist/${eventId}`);
        if (response.status === 200) {
          button.classList.replace("btn-danger", "btn-success");
          button.textContent = "Add to Wishlist";
        }
      }
    } catch (error) {
      console.error("Error updating wishlist:", error);
      alert("An error occurred. Please try again.");
    } finally {
      button.disabled = false;
    }
  }
});
