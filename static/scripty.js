// JavaScript for card animations
const cards = document.querySelectorAll('.card');

cards.forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'scale(1.1)';
        card.style.transition = 'transform 0.3s';
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'scale(1)';
    });
});
// Assuming you have jQuery loaded in your project

$(document).ready(function() {
    // Add a click event listener to all "Vote" buttons
    $("button#vote-button").click(function() {
      // Get the candidate ID or any unique identifier for the candidate
      var candidateId = $(this).closest(".card").data("candidate-id");
  
      // Send an AJAX request to cast the vote
      $.ajax({
        url: "/vote/", // Replace with your actual endpoint URL
        method: "POST",
        data: {
          candidate_id: candidateId,
        },
        success: function(response) {
          if (response.success) {
            // Update the vote count on the page
            var newVoteCount = response.new_vote_count;
            $("#president-votes").text(newVoteCount);
            // You can add a success message or update the button style here
          } else {
            // Handle errors, display an error message, etc.
          }
        },
      });
    });
  });
  