/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tournament;

import games.MatrixGame;
import games.MixedStrategy;

/**
 *
 * @author Klara
 */
public class RepGameSameStrat extends Player {
            protected final String newName = "RepGameSameStrat";

    public RepGameSameStrat() {
            super();
            playerName = newName;
    }

    private class pair{
      double row;
      double column;

      pair(){
        row = Double.MAX_VALUE;
        column = Double.MAX_VALUE;
      }
    }

    private MixedStrategy nashEq(MatrixGame mg, int playerNumber){
      MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
      int act = mg.getNumActions(playerNumber);
      int outcome[] = {1,1};

      pair[][] table = new pair[act][act];

      //print nash eq table
      for(int i = 0; i < act; i++){
        for(int j = 0; j < act; j++){
          table[i][j] = new pair();
        }
      }

      //find nash equilibrium for row player - find best of each column
      for(int col = 1; col <= act; col++){
        outcome[0] = 1;
        outcome[1] = col;

        double max = mg.getPayoff(outcome, 0);
        for(int row = 1; row <= act; row++){
          outcome[0] = row;
          if(mg.getPayoff(outcome, 0) > max){
            max = mg.getPayoff(outcome, 0);
          }
        }
        for(int row = 1; row <= act; row++){ // find positions with max and set them to true
          outcome[0] = row;
          table[row-1][col-1].row = max - mg.getPayoff(outcome, 0);

        }
      }

      //find nash equilibrium for column player
      for(int row = 1; row <= act; row++){
        outcome[0] = row;
        outcome[1] = 1;

        double max = mg.getPayoff(outcome, 1);
        for(int col = 1; col <= act; col++){
          outcome[1] = col;
          if(mg.getPayoff(outcome, 1) > max){
            max = mg.getPayoff(outcome, 1);
          }
        }
        for(int col = 1; col <= act; col++){ // find positions with max and set them to true
          outcome[1] = col;
          table[row-1][col-1].column = max - mg.getPayoff(outcome, 1);
        }
      }

      //find nash equilibrium
      double maxPlayer = 0.0;
      int action = -1;
      double minDev = Double.MAX_VALUE;

      for(int i = 0; i < act; i++){
        for(int j = 0; j < act; j++){
          //check if it is a nash equilibrium

          if(minDev > table[i][j].row + table[i][j].column){
            outcome[0] = i+1;
            outcome[1] = j+1;
            if(action == -1 || maxPlayer < mg.getPayoff(outcome, playerNumber)){
              if(playerNumber == 0) action = i+1;
              else action = j+1;
              maxPlayer = mg.getPayoff(outcome, playerNumber);
            }
          }

        }
      }
      //set probability 1 to maxPlayer and 0 to the others
      ms.setZeros();
      ms.setProb(action, 1.0);
      return ms;
    }

    protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
        MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
        int numberOfActions = mg.getNumActions(playerNumber);

                //cooperate in the first game - play nash equilibrium
        if(getCurrentRepeatCount() == 0){
            ms = nashEq(mg, playerNumber);
            return ms;
        }


        int posPlayed = 1;
        double prob = 0.0;
         int firstPos;
        MixedStrategy strats[] = new MixedStrategy[mg.getNumPlayers()];
        for(int i = getCurrentRepeatCount(); i < history.size(); i++){
                if(playerNumber == 0) firstPos = 1;
                else firstPos = 0;
                for(int p = firstPos; p < strats.length; p+=2){
                    if(p >= strats.length) break;
                    strats[p] = history.get(i)[p];

                    for(int j = 1; j <= numberOfActions; j++){
                        if(strats[p].getProb(j) > prob){
                            prob = strats[p].getProb(j);
                            posPlayed = j;
                        }
                    }

                }
        }
        int lastChosenPos = 1;
        //get my last chosen position
        if(playerNumber == 0) firstPos = 0;
                else firstPos = 1;
                for(int p = firstPos; p < strats.length; p+=2){
                    if(p >= strats.length) break;
                    strats[p] = history.get(history.size()-1)[p];
                    for(int j = 1; j <= numberOfActions; j++){
                        if(strats[p].getProb(j) == 1){
                            lastChosenPos = j;
                        }
                    }

        }

        if(playerNumber == 0){ //choose the row with the highest outcome
            //check last outcome if it was lower than the expected one, choose second highest
            double realOutcome = lastPayoffs[0];
            int outcome[] = {1,1};
            outcome[0] = lastChosenPos;
            outcome[1] = posPlayed;
          //  double realOutcome = lastOutcome;
            double expectedPayoff = mg.getPayoff(outcome, playerNumber);

            int maxRow = 1;
            double maxValue = -100.0;
            for(int row = 1; row <= numberOfActions; row++){
                outcome[0] = row;
                outcome[1] = posPlayed;
                double payoff = mg.getPayoff(outcome, playerNumber);
                if(payoff == expectedPayoff) payoff = realOutcome;
                if(payoff > maxValue){
                    maxValue = payoff;
                    maxRow = row;
                }
            }
            //check if row minimum is bigger than current minimum
            System.out.println("playing row: " + maxRow);
            ms.setZeros();
            ms.setProb(maxRow, 1.0);
        } else if(playerNumber == 1){ //choose column with the highest outcome
                        //check last outcome if it was lower than the expected one, choose second highest
            double realOutcome = lastPayoffs[0];
            int outcome[] = {1,1};
            outcome[0] = posPlayed;
            outcome[1] = lastChosenPos;
          //  double realOutcome = lastOutcome;
            double expectedPayoff = mg.getPayoff(outcome, playerNumber);

            int maxColumn = 0;
            double maxValue = -100.0;
            for(int col = 1; col <= numberOfActions; col++){
                outcome[0] = posPlayed;
                outcome[1] = col;
                double payoff = mg.getPayoff(outcome, playerNumber);
               if(payoff == expectedPayoff) payoff = realOutcome;
            if(payoff > maxValue){
                System.out.println(payoff + " " + maxValue);
                maxValue = payoff;
                maxColumn = col;
            }
        }
        //check if row minimum is bigger than current minimum
        System.out.println("playing column: " +maxColumn );
        ms.setZeros();
        ms.setProb(maxColumn, 1.0);
    }
    return ms;
    }


}
