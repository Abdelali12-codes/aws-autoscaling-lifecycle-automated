aws autoscaling complete-lifecycle-action \
          --lifecycle-hook-name AutoScalingHook \
          --auto-scaling-group-name aws-cloudformation-autoscaling \
          --lifecycle-action-result CONTINUE \
          --instance-id   i-0e1f621c9710e22c6 \
          --region eu-west-3