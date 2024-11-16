from enum import Enum
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
import json

class StepType(Enum):
    PROCESS = "process"
    DECISION = "decision" 
    TERMINAL = "terminal"

@dataclass
class Step:
    name: str
    step_type: StepType
    instruction: str
    connections: List[str]
    
class Stage1Generator:
    """Conceptual splitting of the prompt into structured workflow steps"""
    
    def __init__(self):
        self.steps: List[Step] = []
        
    def generate_workflow(self, prompt: str) -> List[Step]:
        # Parse natural language prompt into structured steps
        concepts = self._extract_key_concepts(prompt)
        return self._create_workflow_steps(concepts)
    
    def _extract_key_concepts(self, prompt: str) -> List[str]:
        # Extract main concepts/tasks from the prompt
        # This would use NLP techniques in practice
        concepts = []
        current_concept = ""
        for line in prompt.split('\n'):
            if line.strip():
                concepts.append(line)
        return concepts

    def _create_workflow_steps(self, concepts: List[str]) -> List[Step]:
        workflow = []
        for i, concept in enumerate(concepts):
            step_type = self._determine_step_type(concept)
            connections = [f"step_{i+2}"] if i < len(concepts)-1 else []
            
            workflow.append(Step(
                name=f"step_{i+1}",
                step_type=step_type,
                instruction=concept,
                connections=connections
            ))
        return workflow

    def _determine_step_type(self, concept: str) -> StepType:
        if "?" in concept:
            return StepType.DECISION
        elif concept.lower().startswith(("finish", "end", "complete")):
            return StepType.TERMINAL
        return StepType.PROCESS

class Stage2Generator:
    """Converts workflow into pseudocode-like representation"""
    
    def generate_pseudocode(self, workflow: List[Step]) -> str:
        pseudocode = []
        
        for step in workflow:
            if step.step_type == StepType.PROCESS:
                pseudocode.append(f"process {step.name}:")
                pseudocode.append(f"    execute: {step.instruction}")
                
            elif step.step_type == StepType.DECISION:
                pseudocode.append(f"decision {step.name}:")
                pseudocode.append(f"    condition: {step.instruction}")
                for conn in step.connections:
                    pseudocode.append(f"    if true: goto {conn}")
                    
            elif step.step_type == StepType.TERMINAL:
                pseudocode.append(f"terminal {step.name}:")
                pseudocode.append(f"    end: {step.instruction}")
                
            if step.connections and step.step_type != StepType.DECISION:
                pseudocode.append(f"    next: {step.connections[0]}")
            pseudocode.append("")
            
        return "\n".join(pseudocode)

class Stage3Evaluator:
    """Handles algorithmic evaluation of the workflow"""
    
    def evaluate_workflow(self, workflow: List[Step], context: Dict) -> float:
        reward = 0.0
        current_step = workflow[0]
        
        while current_step:
            # Execute step and get intermediate reward
            step_reward = self._execute_step(current_step, context)
            reward += step_reward
            
            # Handle transitions
            if current_step.step_type == StepType.TERMINAL:
                break
            elif current_step.step_type == StepType.DECISION:
                condition_met = self._evaluate_condition(current_step, context)
                next_step = workflow[int(current_step.connections[0].split('_')[1])-1] if condition_met else None
            else:
                next_step = workflow[int(current_step.connections[0].split('_')[1])-1] if current_step.connections else None
            
            current_step = next_step
            
        return reward

    def _execute_step(self, step: Step, context: Dict) -> float:
        # Simplified reward calculation
        reward = 0.1  # Base reward for step execution
        
        if step.step_type == StepType.PROCESS:
            reward += 0.2
        elif step.step_type == StepType.DECISION:
            reward += 0.3
        elif step.step_type == StepType.TERMINAL:
            reward += 0.4
            
        return reward

    def _evaluate_condition(self, step: Step, context: Dict) -> bool:
        # Simplified condition evaluation
        return True

class AutoFlowV2:
    def __init__(self):
        self.stage1 = Stage1Generator()
        self.stage2 = Stage2Generator()
        self.stage3 = Stage3Evaluator()
        
    def process_workflow(self, prompt: str, context: Dict = None) -> tuple:
        if context is None:
            context = {}
            
        # Stage 1: Generate workflow
        workflow = self.stage1.generate_workflow(prompt)
        
        # Stage 2: Generate pseudocode
        pseudocode = self.stage2.generate_pseudocode(workflow)
        
        # Stage 3: Evaluate
        reward = self.stage3.evaluate_workflow(workflow, context)
        
        return workflow, pseudocode, reward

# Example usage
if __name__ == "__main__":
    autoflow = AutoFlowV2()
    
    test_prompt = """
    Identify input data type
    Process the data according to type
    Check if processing was successful
    Output results
    """
    
    workflow, pseudocode, reward = autoflow.process_workflow(test_prompt)
    print(f"Generated Pseudocode:\n{pseudocode}")
    print(f"Workflow Reward: {reward}")