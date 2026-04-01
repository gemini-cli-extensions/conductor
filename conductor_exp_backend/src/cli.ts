#!/usr/bin/env node
import { initMasterSpec, addSubSpec, runImpactAnalysis } from './manageSpec.js';
import { initSession, createSessionPlan, createSessionTask, visualizeDAG } from './orchestration.js';

async function run() {
    const command = process.argv[2];
    const args = process.argv.slice(3);

    console.log(`Running CLI Command: ${command} with args: ${args.join(', ')}`);

    try {
        switch (command) {
            case 'init-session':
                const [sessId] = args;
                console.log(await initSession(sessId));
                break;
            case 'init':
                // Usage: init <specId> <goal> <requirements...>
                const [initSpecId, initGoal, ...initReqs] = args;
                console.log(await initMasterSpec(initSpecId, initGoal, initReqs, [])); // Empty verifiers for now
                break;
            case 'sub':
                // Usage: sub <specId> <parentId> <goal> <requirements...>
                const [subSpecId, parentId, subGoal, ...subReqs] = args;
                console.log(await addSubSpec(subSpecId, parentId, subGoal, subReqs, []));
                break;
            case 'plan':
                // Usage: plan [sessionId] <planId> <goal> <specId>
                let planSessionId: string | undefined;
                let [pId, pGoal, pSpecId] = args;
                if (args.length === 4) {
                    [planSessionId, pId, pGoal, pSpecId] = args;
                }
                console.log(await createSessionPlan(planSessionId, pId, pGoal, pSpecId));
                break;
            case 'task':
                // Usage: task [sessionId] <taskId> <description> <planId>
                let taskSessionId: string | undefined;
                let [tId, tDesc, tPlanId] = args;
                if (args.length === 4) {
                    [taskSessionId, tId, tDesc, tPlanId] = args;
                }
                console.log(await createSessionTask(taskSessionId, tId, tDesc, tPlanId));
                break;
            case 'graph':
                console.log(await visualizeDAG());
                break;
            case 'analyze':
                console.log(await runImpactAnalysis());
                break;
            default:
                console.log("Unknown command or missing arguments.");
                console.log("Usage: node cli.js <command> [args]");
                console.log("Commands: init-session, init, sub, plan, task, graph, analyze, edit, merge");
                break;
        }
        process.exit(0);
    } catch (e: any) {
        console.error(`\n❌ Command Failed:`, e.message);
        process.exit(1);
    }
}

run();
