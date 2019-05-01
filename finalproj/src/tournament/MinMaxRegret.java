/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tournament;

import games.MatrixGame;
import games.MixedStrategy;
import tournament.Player;

/**
 *
 * @author Klara
 */
public class MinMaxRegret extends Player {
    protected final String newName = "MinMaxRegret";

    public MinMaxRegret() {
        super();
        playerName = newName;
    }

    protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
        MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
        int act = mg.getNumActions(playerNumber);
        int outcome[] = {1,1};
        double payoffMaxMin = Double.MIN_VALUE;
        int chosenPosition = 1;
        double [][] regretTable = new double[act][act];

        //row player
        if(playerNumber == 0){
            //calculate regret table
            for(int col = 1; col <= act; col++){
                outcome[0] = 1;
                outcome[1] = col;
                double highest = mg.getPayoff(outcome, playerNumber);
                for(int row = 1; row <= act; row++){ //find highest number of the column
                    outcome[0] = row;
                    outcome[1] = col;
                    if(mg.getPayoff(outcome, playerNumber) > highest){
                        highest = mg.getPayoff(outcome, playerNumber);
                    }
                } //fill in column of the regret table
                for(int r = 0; r < act; r++){
                    outcome[0] = r+1;
                    regretTable[r][col-1] = highest - mg.getPayoff(outcome, playerNumber);
                }
            }
            //get maximum of each row of the regret table
            double [] max = new double[act];
            for(int row = 0; row < act; row++){
                double rowMax = regretTable[row][0];
                for(int col = 0; col < act; col++){
                    if(regretTable[row][col] > rowMax){
                        rowMax = regretTable[row][col];
                    }
                }
                max[row] = rowMax;
            }
            //find minimum of the maximums
            double min = max[0];
            for(int i = 0; i < act; i++){
                if(max[i] < min){
                    min = max[i];
                    chosenPosition = i+1;
                }
            }
        }
        else if(playerNumber == 1){ //column player
            //calculate regret table
            for(int row = 1; row <= act; row++){
                outcome[0] = row;
                outcome[1] = 1;
                double highest = mg.getPayoff(outcome, playerNumber);
                for(int col = 1; col <= act; col++){ //find highest number of the column
                    outcome[0] = row;
                    outcome[1] = col;
                    if(mg.getPayoff(outcome, playerNumber) > highest){
                        highest = mg.getPayoff(outcome, playerNumber);
                    }
                } //fill in column of the regret table
                for(int r = 0; r < act; r++){
                    outcome[0] = r+1;
                    regretTable[row-1][r] = highest - mg.getPayoff(outcome, playerNumber);
                }
            }
            //get maximum of each row of the regret table
            double [] max = new double[act];
            for(int col = 0; col < act; col++){
                double rowMax = regretTable[0][col];
                for(int row = 0; row < act; row++){
                    if(regretTable[row][col] > rowMax){
                        rowMax = regretTable[row][col];
                    }
                }
                max[col] = rowMax;
            }
            //find minimum of the maximums
            double min = max[0];
            for(int i = 0; i < act; i++){
                if(max[i] < min){
                    min = max[i];
                    chosenPosition = i+1;
                }
            }
        }
        ms.setZeros();
        ms.setProb(chosenPosition, 1.0);
        return ms;
    }



}
