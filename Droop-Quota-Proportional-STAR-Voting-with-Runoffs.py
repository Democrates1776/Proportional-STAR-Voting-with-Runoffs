# Online Python compiler (interpreter) to run Python online.
import pandas as pd
import numpy as np
 
    #Credit to https://electowiki.org/wiki/Allocated_Score
    #Allocated Score is another name for STAR-PR
    
def gather_input():
    num_candidates = int(input("Enter the number of candidates: "))
    candidate_names = []
    for i in range(num_candidates):
        name = input(f"Enter the name of candidate {i+1}: ")
        candidate_names.append(name)

    num_seats = int(input("Enter the number of seats: "))

    scores_input = input("Enter all the ballots separated by space with no space within each ballot e.g. 231 215 421 (for all voters, every group of {} numbers without spaces represents one voter's ballot.): ".format(num_candidates))
    scores_list = scores_input.split()

    num_voters = len(scores_list)
    print("\nThere are ", num_voters, " voters.")
    scores_matrix = np.zeros((num_voters, num_candidates), dtype=int)

    for i in range(num_voters):
        ballot = scores_list[i]
        if len(ballot) != num_candidates:
            raise ValueError(f"Invalid ballot: {ballot}. Each ballot should have {num_candidates} scores.")
        scores_matrix[i] = [int(score) for score in ballot]

    return pd.DataFrame(scores_matrix, columns=candidate_names), num_seats

def allocated_score(ballots, seats):
    max_score = 5 # Maximum score is always 5
    voters, _ = ballots.shape
    quota = int(voters / (seats + 1)) + 1
    ballot_weight = pd.Series(np.ones(voters), name="weights")
    winner_list = []
    round_num = 1

    while len(winner_list) < seats:
        print(f"\nRound {round_num}:\n\nScores:")
        weighted_scores = ballots.multiply(ballot_weight, axis="index")
        total_scores = weighted_scores.sum()

        for candidate, score in total_scores.sort_values(ascending=False).items():
            formatted_score = "{:.4f}".format(score).rstrip('0').rstrip('.')
            print(f"{candidate}: {formatted_score}")

        # Determine the top 2 candidates for the runoff
        top_2 = total_scores.nlargest(2).index.tolist()

        # Perform the runoff
        runoff_votes = pd.Series(np.zeros(2), index=top_2)
        no_preference_count = 0
        for _, ballot in ballots[top_2].iterrows():
            if ballot_weight[_] > 0:
                if ballot[top_2[0]] > ballot[top_2[1]]:
                    runoff_votes[top_2[0]] += ballot_weight[_]
                elif ballot[top_2[0]] < ballot[top_2[1]]:
                    runoff_votes[top_2[1]] += ballot_weight[_]
                else:
                    no_preference_count += ballot_weight[_]

        print("\nRunoff votes:")
        for candidate, votes in runoff_votes.items():
            formatted_votes = "{:.4f}".format(votes).rstrip('0').rstrip('.')
            print(f"{candidate}: {formatted_votes}")

        print(f"No preference: {no_preference_count:.4f}".rstrip('0').rstrip('.'))

        winner = runoff_votes.idxmax()
        winner_list.append(winner)
        ballots.drop(winner, axis=1, inplace=True)

        cand_df = pd.concat([ballot_weight, weighted_scores[winner]], axis=1).copy()
        cand_df_sort = cand_df.sort_values(by=[winner], ascending=False).copy()
        split_point = cand_df_sort[cand_df_sort["weights"].cumsum() < quota][winner].min()
        spent_above = cand_df[cand_df[winner] > split_point]["weights"].sum()

        if spent_above > 0:
            cand_df.loc[cand_df[winner] > split_point, "weights"] = 0.0
        weight_on_split = cand_df[cand_df[winner] == split_point]["weights"].sum()
        if weight_on_split > 0:
            spent_value = (quota - spent_above) / weight_on_split
            cand_df.loc[cand_df[winner] == split_point, "weights"] *= (1 - spent_value)

        ballot_weight = cand_df["weights"].clip(0.0, 1.0)

        round_num += 1

    return winner_list

# Main part of the script
if __name__ == "__main__":
    ballots, seats = gather_input()
    winners = allocated_score(ballots, seats)
    print("\nWinners:", winners)
