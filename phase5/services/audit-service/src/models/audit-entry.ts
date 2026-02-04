import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

export enum AuditAction {
  CREATED = 'CREATED',
  UPDATED = 'UPDATED',
  COMPLETED = 'COMPLETED',
  DELETED = 'DELETED'
}

@Entity('audit_entries')
export class AuditEntry {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ type: 'uuid' })
  taskId: string;

  @Column({ type: 'uuid' })
  userId: string;

  @Column({
    type: 'enum',
    enum: AuditAction
  })
  action: AuditAction;

  @Column({ type: 'jsonb' })
  beforeState: any;

  @Column({ type: 'jsonb' })
  afterState: any;

  @Column({ type: 'text' })
  changedFields: string;

  @CreateDateColumn()
  createdAt: Date;

  @Column({ type: 'text', nullable: true })
  sourceService: string;
}