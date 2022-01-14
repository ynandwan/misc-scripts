 

cd /home/cse/phd/csz178057/phd/temprels/distant_temprel_pub/
rm /home/yatin/phd/misc-scripts/hpcv2/hpc_jobs/rrn_equal_abl_rep/JACK_11
/home/cse/phd/csz178057/.conda/envs/tr3/bin/python train_curriculum.py  --data matres --lm roberta --early_stop_data matres_dev_sup --eval_data matres_dev_sup matres_test_sup.constrained_tc --subselect_triples 0  --concat_tokens 1 --nbr_s 0 --nbr_e 0  --train_style sup --model_type ft --lambda_warmup_fraction 0.0 --seed 9834 --num_unsup 0 --num_sup -1 --aug_trans 1 --rev_reg 1 --sym_loss_lambda 0 --trans_loss_lambda 0 --batch 8 --filter_annotated 1 --aug_num_sentences 1000 --num_sentences 2 --epochs 10 --num_evals 20 --output_dir sb3_trained_models/rrn_equal_abl_rep/ans-1000_agtr-1_b-8_e-10_fa-1_lwf-0.0_mt-ft_ne-20_ns-2_ns-.1_nu-0_rr-1_s-9834_sll-0_tll-0 &
pids[0]=$!
for pid in ${pids[*]}; do 
         wait $pid 
done

touch /home/yatin/phd/misc-scripts/hpcv2/hpc_jobs/rrn_equal_abl_rep/JACK_11
