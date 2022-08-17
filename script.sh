aws autoscaling complete-lifecycle-action \
          --lifecycle-hook-name AutoScalingHook \
          --auto-scaling-group-name aws-cloudformation-autoscaling \
          --lifecycle-action-result CONTINUE \
          --instance-id  i-059d840d166591e5d \
          --region eu-west-3