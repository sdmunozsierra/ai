/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tournament;
import games.*;
import java.util.Arrays;
import util.SolverUtils;


/**
 *
 * @author Klara
 */
public class MaxMinPayoff extends Player{
    	protected final String newName = "MaxMinPayoff";

	public MaxMinPayoff() {
		super();
        playerName = newName;
	}

      /**
     * GameMaster will call this to compute your strategy.
     * @param mg The game your agent will be playing
     * @param playerNumber Row Player = 1, Column Player = 2
     */
    protected MixedStrategy solveGame(MatrixGame mg, int playerNumber){
        MixedStrategy ms = new MixedStrategy(mg.getNumActions(playerNumber));
        int act = mg.getNumActions(playerNumber);
        int outcome[] = {0,0};
        double payoffMaxMin = Double.MIN_VALUE;
        int chosenAction = -1;

        //for row player
        if(playerNumber == 0){
            for(int row = 1; row <= act; row++){
                double min = Double.MAX_VALUE;
                //get minimum of the row
                for(int col = 1; col <= act; col++){
                    outcome[0] = row;
                    outcome[1] = col;
                    if(mg.getPayoff(outcome, playerNumber) < min)
                        min = mg.getPayoff(outcome, playerNumber);
                }
                //check if row minimum is bigger than current minimum
                if(chosenAction == -1 || payoffMaxMin < min) {
                    payoffMaxMin = min;
                    chosenAction = row;
                }
            }
        } else if(playerNumber == 1){
            for(int col = 1; col <= act; col++){
                double min = Double.MAX_VALUE;
                //get minimum of the row
                for(int row = 1; row <= act; row++){
                    outcome[0] = row;
                    outcome[1] = col;
                    if(mg.getPayoff(outcome, playerNumber) < min)
                        min = mg.getPayoff(outcome, playerNumber);
                }
                //check if row minimum is bigger than current minimum
                if(chosenAction == -1 || payoffMaxMin < min) {
                    payoffMaxMin = min;
                    chosenAction = col;
                }
            }
        }
        else {
            System.out.println("Non-specified player " + playerNumber);
        }
        for(int i = 1; i <= mg.getNumActions(playerNumber); i++){
            if(i != chosenAction) ms.setProb(i, 0);
            else  ms.setProb(i, 1.0);
       }
        return ms;
   }

}
