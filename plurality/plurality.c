// Calculates winner of plurality elections

#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // Matches name input by a voter with the array of candidates
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1; // Updates candidates vote total to aacount for a new vote
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    int winners[MAX] = {0};  // New array populated by indices of winner(s) in the main array
    int n = 0;  // Variable counting multiple winners
    int record = 0; // Variable for counting maximum number of votes

    for (int i = 0; i < candidate_count; i++) // Checking for the highest numer of votes
    {
        if (candidates[i].votes > record)
        {
            record = candidates[i].votes;
        }
    }

    for (int i = 0; i < candidate_count; i++) // Checking for multiple winners
    {
        if (candidates[i].votes == record)
        {
            winners[n] = i;
            n++;
        }
    }

    for (int i = 0; i < n; i++) // Printing names
    {
        printf("%s\n", candidates[winners[i]].name);
    }
    return;
}